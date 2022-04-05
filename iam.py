
import json
from subprocess import call
from urllib import response
from header import HEADER, token
from singleton import Singleton
from call_api import call_api


class IamHandler(metaclass=Singleton):

    def __init__(self):
        self.url = "https://id-admin-dgl.vnpayapis.com/api/v1.0"

    def create_role_group(self, name: str, code: str):
        body = {
            "name": name,
            "code": code
        }
        call_api(self.url + "/role_groups",method='post', json=body, token_iam=HEADER["authorization"])

    def get_role_group_id(self, email):
        response = call_api(
            "https://id-admin-dgl.vnpayapis.com/api/v1.0/role_groups?page=1&size=10",
            params={
                "name": email
            },
            token_iam=HEADER["authorization"]
        )
        return response.json().get("items")[0].get("id")
    
    def add_role_sale_sale_leader_role(self, role_group_id):
        call_api(
            f"https://id-admin-dgl.vnpayapis.com/api/v1.0/role_groups/{role_group_id}/roles",
            method="post",
            json={
                "role_group_id": role_group_id,
                "role_ids": [36,37]
            },
            token_iam=HEADER["authorization"]
        )

    def add_orgchart_team_id(self, role_group_id, team_ids):
        call_api(
            f"https://id-admin-dgl.vnpayapis.com/api/v1.0/role_groups/{role_group_id}",
            method="put",
            json={"attributes":{"orgChartTeamIds":team_ids}},
            token_iam=HEADER["authorization"]
        )
    
    def get_staff_id_by_email(self,email):
        return call_api(
            f"https://id-admin-dgl.vnpayapis.com/api/v1.0/users?page=1&size=10&email={email}",
            token_iam=HEADER["authorization"]
        ).json().get("items")[0].get("id")