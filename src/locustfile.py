# This locust load test script will simulate users accessing endpoints in the SB API.
#
# Each API endpoint invocation is represented by a `@task(weight)` annotation,
# where `weight`` represents relative frequency of random invocations of different endpoints.

import random

from locust import HttpUser, between, task

from src.utils import API_BASE_URL, API_HEADERS

PAGE_SIZE = 10


class StudyBuilder(HttpUser):
    host = API_BASE_URL

    wait_time = between(1, 3)

    def on_start(self):
        print("==== User joins =====")
        # start by waiting so that the simulated users
        # won't all arrive at the same time
        self.wait()
        self.study_uids = self.list_studies()

    def list_studies(self):
        url = "/studies?page_size=1000"
        response = self.client.get(url, headers=API_HEADERS, verify=False)

        # Return list of uid for studies
        studies = response.json()["items"]
        return [study["uid"] for study in studies]

    @task(100)
    def get_soa(self):
        # Pick a random study in the list
        # And then make some API calls with it
        study_uid = random.choice(self.study_uids)

        try:
            self.client.get(f"/studies/{study_uid}", headers=API_HEADERS, verify=False)
            self.client.get(
                f"/studies/{study_uid}/time-units?for_protocol_soa=true",
                headers=API_HEADERS,
                verify=False,
            )
            self.client.get(
                f"/studies/{study_uid}/soa-preferences",
                headers=API_HEADERS,
                verify=False,
            )
            self.client.get(
                "/ct/terms?page_size=100&sort_by=%7B%22name.sponsor_preferred_name%22:true%7D&codelist_name=Footnote+Type",
                headers=API_HEADERS,
                verify=False,
            )
            self.client.get(
                f"/studies/{study_uid}/study-activities?page_size=0&page_number=1",
                headers=API_HEADERS,
                verify=False,
            )
            self.client.get(
                f"/studies/{study_uid}/study-visits?page_size=0&filters=%7B%22consecutive_visit_group%22:%7B%22v%22:[null],%22op%22:%22eq%22%7D,%22visit_class%22:%7B%22v%22:[%22NON_VISIT%22,%22UNSCHEDULED_VISIT%22],%22op%22:%22ne%22%7D%7D",
                headers=API_HEADERS,
                verify=False,
            )
            self.client.get(
                f"/studies/{study_uid}/flowchart?detailed=true",
                headers=API_HEADERS,
                verify=False,
            )
            self.client.get(
                f"/studies/{study_uid}/study-soa-footnotes?page_number=1&page_size=0&total_count=true",
                headers=API_HEADERS,
                verify=False,
            )
        except Exception as e:
            print("An error occurred: ", str(e))
