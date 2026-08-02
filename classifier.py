from rules import detect_message_type


# -------------------------------------------------
# Confidence Calculator
# -------------------------------------------------

def calculate_confidence(message_type, context):

    score = 0.55

    if context["business"] is not None:
        score += 0.10

    if context["relationship"] is not None:
        score += 0.10

    if context["group"] is not None:
        score += 0.05

    if message_type in ["urgent", "payment"]:
        score += 0.15

    if message_type in ["scam", "forward"]:
        score += 0.15

    user = context["user"]

    if user is not None:
        if user["messages_opened_30d"] > 40:
            score += 0.05
        if user["notifications_dismissed_30d"] > 20:
            score -= 0.05

    if (
        context["business"] is not None
        and context["relationship"] is not None
        and message_type == "payment"
    ):
        score += 0.08

    return min(score, 0.99)



# -------------------------------------------------
# Reason Generator
# -------------------------------------------------

def generate_reason(message_type, context):

    reasons = []

    if context["business"] is not None:
        if context["business"]["verified"] == 1:
            reasons.append("verified business")

    if context["relationship"] is not None:
        reasons.append("existing relationship")

    if context["group"] is not None:
        reasons.append(context["group"]["group_type"] + " group")

    reasons.append(message_type.replace("_", " "))

    return ", ".join(reasons)


# -------------------------------------------------
# Main Decision Engine
# -------------------------------------------------

def decide_action(message, context):

    message_type = detect_message_type(
        message["message_text"],
        message["conversation_type"],
        message["forwarded_count"]
    )

    group = context["group"]
    business = context["business"]
    relationship = context["relationship"]
    member = context["group_member"]
    user = context["user"]

    confidence = calculate_confidence(
        message_type,
        context
        
    )

    reason = generate_reason(
        message_type,
        context
    )

    # -----------------------------------------
    # Scam / Spam
    # -----------------------------------------
    if message["forwarded_count"] >= 10:
        return (
            "mute",
            message_type,
            "Highly forwarded message",
            0.99
    )

    if message_type in ["scam", "forward"]:
        return (
            "mute",
            message_type,
            reason,
            confidence
        )

    # -----------------------------------------
    # Do Not Disturb
    # -----------------------------------------
    if user is not None:
        dnd = user["do_not_disturb_window"]
        if message_type not in ["urgent", "payment"]:
            hour = int(str(message["created_at"]).split(" ")[1].split(":")[0])

            start = int(dnd.split("-")[0].split(":")[0])

            end = int(dnd.split("-")[1].split(":")[0])

            if start > end:
                if hour >= start or hour < end:
                    return(
                        "digest",
                        message_type,
                        "User is in Do Not Disturb period",
                        confidence
                )

    # -----------------------------------------
    # Personal Chats
    # -----------------------------------------

    if message["conversation_type"] == "personal":

        if message_type in ["urgent", "payment"]:
            return (
                "notify",
                message_type,
                reason,
                confidence
            )

        return (
            "notify",
            message_type,
            reason,
            confidence
        )

    # -----------------------------------------
    # Group Chats
    # -----------------------------------------

    if message["conversation_type"] == "group":

        if member is not None:

            if member["group_muted_by_user"] == 1:

                if message_type not in ["urgent", "payment"]:
                    return (
                        "digest",
                        message_type,
                        "Muted group",
                        confidence
                    )

        if group is not None:

            if group["group_type"] == "family":
                return (
                    "notify",
                    message_type,
                    reason,
                    confidence
                )

            elif group["group_type"] == "work":

                if message_type in [
                    "urgent",
                    "payment",
                    "event"
                ]:
                    return (
                        "notify",
                        message_type,
                        reason,
                        confidence
                    )

                return (
                    "digest",
                    message_type,
                    reason,
                    confidence
                )

            elif group["group_type"] in [
                "school",
                "college"
            ]:

                if message_type in [
                    "urgent",
                    "payment",
                    "event"
                ]:
                    return (
                        "notify",
                        message_type,
                        reason,
                        confidence
                    )

                return (
                    "digest",
                    message_type,
                    reason,
                    confidence
                )

            elif group["group_type"] == "society":

                if message_type in [
                    "payment",
                    "urgent"
                ]:
                    return (
                        "notify",
                        message_type,
                        reason,
                        confidence
                    )

                return (
                    "digest",
                    message_type,
                    reason,
                    confidence
                )

        return (
            "digest",
            message_type,
            reason,
            confidence
        )

    # -----------------------------------------
    # Business Chats
    # -----------------------------------------

    if message["conversation_type"] == "business":

        if business is not None:

            if business["verified"] == 1:

                if message_type in [
                    "urgent",
                    "payment"
                ]:
                    return (
                        "notify",
                        message_type,
                        reason,
                        confidence
                    )

                if message_type == "business_update":

                    if relationship is not None:
                        return (
                            "notify",
                            message_type,
                            reason,
                            confidence
                        )

                    return (
                        "digest",
                        message_type,
                        reason,
                        confidence
                    )

                if message_type == "promotion":

                    if relationship is not None:

                        if relationship["allows_promotions"] == 1:
                            return (
                                "digest",
                                message_type,
                                reason,
                                confidence
                            )

                        return (
                            "mute",
                            message_type,
                            reason,
                            confidence
                        )

                    return (
                        "digest",
                        message_type,
                        reason,
                        confidence
                    )

                return (
                    "digest",
                    message_type,
                    reason,
                    confidence
                )

            else:

                if message_type == "promotion":
                    return (
                        "mute",
                        message_type,
                        reason,
                        confidence
                    )

                return (
                    "digest",
                    message_type,
                    reason,
                    confidence
                )

        return (
            "digest",
            message_type,
            reason,
            confidence
        )

    # -----------------------------------------
    # Default
    # -----------------------------------------

    return (
        "digest",
        message_type,
        reason,
        confidence
    )