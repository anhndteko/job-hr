from email import header
from call_api import call_api
from header import HEADER
from iam import IamHandler


HR_URL = "https://hr.vnpayapis.com/api"


def get_all_sale_admin():
    params = {
        "page": 1,
        "page_size": 1000,
        "role": "sale-admin",
        "type": "list"
    }
    a = call_api(url=HR_URL + "/staffs",
                 token_iam=HEADER["authorization"], params=params)
    return a.json().get("data")


def get_detail_staff(email):
    return call_api(url=HR_URL+f"/staffs/0?email={email}", token_iam=HEADER["authorization"]).json().get("data")


def create_role_group_name_email_admin():

    all_admin = get_all_sale_admin()
    for staff in all_admin:
        email = staff.get("email")
        create_role_group_with_email(email)


def create_role_group_with_email(email):
    name = "[VNNG] " + email
    code = "ticket-bff:" + email
    IamHandler().create_role_group(name=name, code=code)


def add_role_sale_sale_leader():
    iam_srv = IamHandler()
    all_admin = get_all_sale_admin()
    for staff in all_admin:
        email = staff.get("email")
        iam_srv.add_role_sale_sale_leader_role(
            iam_srv.get_role_group_id(email))


def get_role_group_sale_admin():
    iam_srv = IamHandler()
    all_admin = get_all_sale_admin()
    for staff in all_admin:
        email = staff.get("email")
        role_group_id = iam_srv.get_role_group_id(email)
        teams = get_detail_staff(email).get("team")
        team_id = [str(team.get("team_id")) for team in teams]
        print(team_id)
        iam_srv.add_orgchart_team_id(role_group_id, team_id)


def update_role_group_to_sale_admin():
    iam_srv = IamHandler()
    all_admin = get_all_sale_admin()
    for staff in all_admin:
        email = staff.get("email")
        user_id_iam = iam_srv.get_staff_id_by_email(email)


def update_role_group_one_person(email: str):
    iam_srv = IamHandler()
    user_id_iam = iam_srv.get_staff_id_by_email(email)
    create_role_group_with_email(email)
    role_group_id = iam_srv.get_role_group_id(email)
    iam_srv.add_role_sale_sale_leader_role(role_group_id)

    teams = get_detail_staff(email).get("team")
    team_id = [str(team.get("team_id")) for team in teams]
    print(team_id)
    iam_srv.add_orgchart_team_id(role_group_id, team_id)


# update_role_group_one_person('lyntl1@vnpay.vn')
