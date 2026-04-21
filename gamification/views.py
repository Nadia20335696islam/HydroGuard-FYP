"""
Views for the gamification app.

This module manages all user-facing gamification functionality,
including:
- displaying the gamification dashboard
- saving daily mini-game results
- saving daily mission completions
- awarding eco points
- updating levels and streaks
- automatically creating and awarding badges

The gamification features are kept separate from the main dashboard
to preserve a clean and focused user experience.
"""

# --------------------------------------------------
# DJANGO IMPORTS
# --------------------------------------------------
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json

# --------------------------------------------------
# APPLICATION IMPORTS
# --------------------------------------------------
from accounts.models import User
from .models import (
    Badge,
    UserGameProfile,
    UserBadge,
    DailyGameSession,
    DailyMissionCompletion,
)


# --------------------------------------------------
# BADGE DEFINITIONS
# --------------------------------------------------
# These badges are created automatically if they do not
# already exist in the database.
BADGE_DEFINITIONS = [
    {
        "name": "First Drop",
        "description": "Completed your first HydroGuard activity.",
        "icon": "💧",
    },
    {
        "name": "Mission Starter",
        "description": "Completed your first daily water-saving mission.",
        "icon": "✅",
    },
    {
        "name": "Water Hero",
        "description": "Completed the Water Rescue Challenge mini game.",
        "icon": "🦸",
    },
    {
        "name": "Eco Starter",
        "description": "Reached 50 eco points.",
        "icon": "🌱",
    },
    {
        "name": "Eco Champion",
        "description": "Reached 100 eco points.",
        "icon": "🏆",
    },
    {
        "name": "Consistency Saver",
        "description": "Built a 3-day streak.",
        "icon": "🔥",
    },
]


# --------------------------------------------------
# HELPER FUNCTION: ENSURE BADGES EXIST
# --------------------------------------------------
def ensure_default_badges():
    """
    Ensure that all standard HydroGuard badges exist.

    This allows the system to work immediately without requiring
    the administrator to manually create badges in Django admin.
    """
    for badge_data in BADGE_DEFINITIONS:
        Badge.objects.get_or_create(
            name=badge_data["name"],
            defaults={
                "description": badge_data["description"],
                "icon": badge_data["icon"],
            }
        )


# --------------------------------------------------
# HELPER FUNCTION: AWARD A BADGE
# --------------------------------------------------
def award_badge_if_missing(user, badge_name, unlocked_badges):
    """
    Award a badge to the user if it has not already been unlocked.

    Parameters:
        user (User): the user receiving the badge
        badge_name (str): the name of the badge
        unlocked_badges (list): list used to collect newly unlocked badges
    """
    badge = Badge.objects.filter(name=badge_name).first()

    if badge:
        user_badge, created = UserBadge.objects.get_or_create(
            user=user,
            badge=badge
        )

        if created:
            unlocked_badges.append({
                "name": badge.name,
                "description": badge.description,
                "icon": badge.icon or "🏅",
                "unlocked_at": timezone.localtime(user_badge.unlocked_at).strftime("%d %b %Y"),
            })


# --------------------------------------------------
# HELPER FUNCTION: CHECK AND AWARD BADGES
# --------------------------------------------------
def evaluate_and_award_badges(user, game_profile):
    """
    Evaluate the user's current progress and award any badges
    that match the defined milestone conditions.

    Returns:
        list: newly unlocked badges in serialisable dictionary form
    """
    ensure_default_badges()

    unlocked_badges = []

    mission_count = DailyMissionCompletion.objects.filter(user=user).count()
    game_completed = DailyGameSession.objects.filter(user=user, completed=True).exists()

    # First activity badge
    if game_profile.points > 0:
        award_badge_if_missing(user, "First Drop", unlocked_badges)

    # First mission badge
    if mission_count >= 1:
        award_badge_if_missing(user, "Mission Starter", unlocked_badges)

    # Mini game completion badge
    if game_completed:
        award_badge_if_missing(user, "Water Hero", unlocked_badges)

    # Points-based badges
    if game_profile.points >= 50:
        award_badge_if_missing(user, "Eco Starter", unlocked_badges)

    if game_profile.points >= 100:
        award_badge_if_missing(user, "Eco Champion", unlocked_badges)

    # Streak-based badge
    if game_profile.streak_days >= 3:
        award_badge_if_missing(user, "Consistency Saver", unlocked_badges)

    return unlocked_badges


# --------------------------------------------------
# HELPER FUNCTION: SERIALISE EARNED BADGES
# --------------------------------------------------
def get_serialised_earned_badges(user):
    """
    Return all earned badges in a JSON-friendly format so the
    frontend can refresh the badge cabinet dynamically.
    """
    earned_badges = (
        UserBadge.objects
        .filter(user=user)
        .select_related("badge")
        .order_by("-unlocked_at")
    )

    return [
        {
            "name": item.badge.name,
            "description": item.badge.description,
            "icon": item.badge.icon or "🏅",
            "unlocked_at": timezone.localtime(item.unlocked_at).strftime("%d %b %Y"),
        }
        for item in earned_badges
    ]


# --------------------------------------------------
# HELPER FUNCTION: UPDATE STREAK AND LEVEL
# --------------------------------------------------
def update_profile_progress(game_profile, points_to_add):
    """
    Update a user's gamification profile after a successful
    game or mission completion.

    This helper centralises the logic for:
    - adding points
    - updating the daily streak
    - recalculating level
    - updating the last activity date
    """
    today = timezone.localdate()

    if game_profile.last_played_date:
        days_difference = (today - game_profile.last_played_date).days

        if days_difference == 1:
            game_profile.streak_days += 1
        elif days_difference == 0:
            pass
        else:
            game_profile.streak_days = 1
    else:
        game_profile.streak_days = 1

    game_profile.points += points_to_add
    game_profile.last_played_date = today
    game_profile.update_level()
    game_profile.save()


# --------------------------------------------------
# GAMIFICATION DASHBOARD VIEW
# --------------------------------------------------
def gamification_dashboard(request):
    """
    Display the gamification dashboard for an authenticated user.

    This view is responsible for:
    - validating the custom session-based login state
    - preventing guest users from accessing personalised gamification data
    - ensuring default badges exist in the database
    - loading or creating the user's game profile
    - re-evaluating badge conditions on every page load
    - retrieving the user's earned badges
    - checking whether today's mini game has already been completed
    - checking which daily missions have already been completed today
    - rendering the gamification dashboard with all required context data
    """
    user_id = request.session.get("user_id")
    is_guest = request.session.get("guest") is True

    if not user_id or is_guest:
        return redirect("accounts:login")

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        request.session.flush()
        return redirect("accounts:login")

    # Ensure all standard badges exist before evaluation.
    ensure_default_badges()

    # Ensure the user always has a gamification profile.
    game_profile, _ = UserGameProfile.objects.get_or_create(user=user)

    # Re-check badge conditions every time the page loads.
    # This fixes cases where the user already had progress
    # before the badge logic was added.
    evaluate_and_award_badges(user, game_profile)

    # Load earned badges after evaluation so the template
    # always receives the latest unlocked badges.
    earned_badges = (
        UserBadge.objects
        .filter(user=user)
        .select_related("badge")
        .order_by("-unlocked_at")
    )

    today = timezone.localdate()

    # Check if today's mini game has already been completed.
    today_session = DailyGameSession.objects.filter(
        user=user,
        play_date=today,
        completed=True
    ).first()

    # Load today's completed daily missions.
    completed_missions = set(
        DailyMissionCompletion.objects.filter(
            user=user,
            play_date=today
        ).values_list("mission_key", flat=True)
    )

    context = {
        "user": user,
        "game_profile": game_profile,
        "earned_badges": earned_badges,
        "today_game_completed": today_session is not None,
        "completed_missions": completed_missions,
    }

    return render(
        request,
        "gamification/gamification_dashboard.html",
        context
    )


# --------------------------------------------------
# SAVE MINI GAME RESULT VIEW
# --------------------------------------------------
@require_POST
def save_game_result(request):
    """
    Save the result of the user's mini-game session.
    """
    user_id = request.session.get("user_id")
    is_guest = request.session.get("guest") is True

    if not user_id or is_guest:
        return JsonResponse(
            {"success": False, "message": "Authentication required."},
            status=403
        )

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        request.session.flush()
        return JsonResponse(
            {"success": False, "message": "Invalid session."},
            status=403
        )

    try:
        data = json.loads(request.body)
        correct_answers = int(data.get("correct_answers", 0))
        total_questions = int(data.get("total_questions", 3))
    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse(
            {"success": False, "message": "Invalid game data received."},
            status=400
        )

    if correct_answers < 0 or total_questions <= 0 or correct_answers > total_questions:
        return JsonResponse(
            {"success": False, "message": "Game result values are invalid."},
            status=400
        )

    today = timezone.localdate()

    existing_session = DailyGameSession.objects.filter(
        user=user,
        play_date=today,
        completed=True
    ).first()

    if existing_session:
        return JsonResponse(
            {"success": False, "message": "You have already completed today's game."},
            status=400
        )

    points_earned = correct_answers * 10
    game_profile, _ = UserGameProfile.objects.get_or_create(user=user)

    update_profile_progress(game_profile, points_earned)

    DailyGameSession.objects.create(
        user=user,
        play_date=today,
        correct_answers=correct_answers,
        total_questions=total_questions,
        points_earned=points_earned,
        completed=True,
    )

    newly_unlocked_badges = evaluate_and_award_badges(user, game_profile)
    earned_badges = get_serialised_earned_badges(user)

    return JsonResponse(
        {
            "success": True,
            "message": "Game result saved successfully.",
            "points_earned": points_earned,
            "total_points": game_profile.points,
            "level": game_profile.level,
            "streak_days": game_profile.streak_days,
            "badge_count": len(earned_badges),
            "newly_unlocked_badges": newly_unlocked_badges,
            "earned_badges": earned_badges,
        }
    )


# --------------------------------------------------
# SAVE DAILY MISSION COMPLETION VIEW
# --------------------------------------------------
@require_POST
def complete_daily_mission(request):
    """
    Save a user's daily mission completion.
    """
    user_id = request.session.get("user_id")
    is_guest = request.session.get("guest") is True

    if not user_id or is_guest:
        return JsonResponse(
            {"success": False, "message": "Authentication required."},
            status=403
        )

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        request.session.flush()
        return JsonResponse(
            {"success": False, "message": "Invalid session."},
            status=403
        )

    try:
        data = json.loads(request.body)
        mission_key = data.get("mission_key", "").strip()
    except (json.JSONDecodeError, TypeError):
        return JsonResponse(
            {"success": False, "message": "Invalid mission data received."},
            status=400
        )

    mission_points = {
        "short_shower": 20,
        "turn_off_tap": 10,
        "smart_dishwashing": 15,
        "log_usage": 10,
    }

    if mission_key not in mission_points:
        return JsonResponse(
            {"success": False, "message": "Selected mission is invalid."},
            status=400
        )

    today = timezone.localdate()

    existing_completion = DailyMissionCompletion.objects.filter(
        user=user,
        mission_key=mission_key,
        play_date=today
    ).first()

    if existing_completion:
        return JsonResponse(
            {"success": False, "message": "You have already completed this mission today."},
            status=400
        )

    points_earned = mission_points[mission_key]
    game_profile, _ = UserGameProfile.objects.get_or_create(user=user)

    update_profile_progress(game_profile, points_earned)

    DailyMissionCompletion.objects.create(
        user=user,
        mission_key=mission_key,
        play_date=today,
        points_earned=points_earned,
    )

    newly_unlocked_badges = evaluate_and_award_badges(user, game_profile)
    earned_badges = get_serialised_earned_badges(user)

    return JsonResponse(
        {
            "success": True,
            "message": "Mission completed successfully.",
            "mission_key": mission_key,
            "points_earned": points_earned,
            "total_points": game_profile.points,
            "level": game_profile.level,
            "streak_days": game_profile.streak_days,
            "badge_count": len(earned_badges),
            "newly_unlocked_badges": newly_unlocked_badges,
            "earned_badges": earned_badges,
        }
    )