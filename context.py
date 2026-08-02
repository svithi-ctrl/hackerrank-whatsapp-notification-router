import pandas as pd


class ContextManager:

    def __init__(self):

        self.users = pd.read_csv("dataset/users.csv")
        self.groups = pd.read_csv("dataset/groups.csv")
        self.group_members = pd.read_csv("dataset/group_members.csv")
        self.business = pd.read_csv("dataset/business_accounts.csv")
        self.user_business = pd.read_csv("dataset/user_business_history.csv")

    def build(self, message):

        context = {}

        # ---------------- User ----------------

        user = self.users[
            self.users.user_id == message.user_id
        ]

        context["user"] = user.iloc[0] if len(user) else None

        # ---------------- Group ----------------

        context["group"] = None

        if pd.notna(message.group_id):

            group = self.groups[
                self.groups.group_id == message.group_id
            ]

            if len(group):
                context["group"] = group.iloc[0]

        # ---------------- Group Membership ----------------

        context["group_member"] = None

        if pd.notna(message.group_id):

            member = self.group_members[
                (self.group_members.user_id == message.user_id)
                &
                (self.group_members.group_id == message.group_id)
            ]

            if len(member):
                context["group_member"] = member.iloc[0]

        # ---------------- Business ----------------

        context["business"] = None

        if pd.notna(message.business_id):

            business = self.business[
                self.business.business_id == message.business_id
            ]

            if len(business):
                context["business"] = business.iloc[0]

        # ---------------- User-Business Relationship ----------------

        context["relationship"] = None

        if pd.notna(message.business_id):

            relation = self.user_business[
                (self.user_business.user_id == message.user_id)
                &
                (self.user_business.business_id == message.business_id)
            ]

            if len(relation):
                context["relationship"] = relation.iloc[0]

        return context