# import typing as tp
#
# from fastapi import APIRouter
# from modules.models import GenericResponse
#
# service_router = APIRouter()
#
#
# @service_router.get("/achievement")
# def get_user_achievements() -> GenericResponse:
#     """Get concrete user's achievements"""
#     pass
#
#
# @service_router.post("/achievement")
# def add_user_achievement() -> GenericResponse:
#     """Add new achievement, accociated with concrete user"""
#     pass
#
#
# @service_router.update("/achievement")
# def update_user_achievement() -> GenericResponse:
#     """Update concrete achievement (only name/type)"""
#     pass
#
#
# @service_router.get("/checkout")
# def get_available_rewards() -> GenericResponse:
#     """Get list of all available rewards"""
#     pass
#
#
# @service_router.post("/checkout")
# def make_purchase() -> GenericResponse:
#     """Purchase reward, change user's balance"""
#     pass
#
#
# @service_router.get("/settings")
# def get_current_settings() -> GenericResponse:
#     """Get list of current settings (evaluations, ratios)"""
#     pass
#
#
# @service_router.update("/settings")
# def update_settings() -> GenericResponse:
#     """Update ratios, weights"""
#     pass
