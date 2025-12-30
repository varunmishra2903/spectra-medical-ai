from backend.core.logging import get_logger

logger = get_logger(__name__)

ALLOWED_ROUTES = {"brain", "chest", "bone"}


class RoutingError(Exception):
    pass


def route_case(gatekeeper_result: str) -> str:
    """
    Locks the processing route for the case.
    """

    logger.info(f"Gatekeeper result: {gatekeeper_result}")

    if gatekeeper_result == "ambiguous":
        logger.error("Routing failed: ambiguous input")
        raise RoutingError(
            "Unable to determine scan type with sufficient confidence"
        )

    if gatekeeper_result not in ALLOWED_ROUTES:
        raise RoutingError(f"Invalid route: {gatekeeper_result}")

    logger.info(f"Route locked: {gatekeeper_result}")
    return gatekeeper_result
