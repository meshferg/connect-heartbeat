import datetime
import pandas as pd
import requests

class ConnectHeartbeat:
    """ConnectHeartbeat class to interface with API endpoint, retrieve data, parse it into useful variables, and
    provide a pandas.DataFrame."""

    def __init__(self, demo_mode: bool=False):
        # Set some variables
        self.heartbeat_api_url = 'https://us-central1-nih-nci-dceg-connect-dev.cloudfunctions.net/heartbeat'
        self.heartbeat_data: str | None = None
        self.last_heartbeat_date: datetime.datetime | None = None
        self.active_participant_count: int | None = None
        self.participant_demo_df: pd.DataFrame | None = None
        self.demo_mode: bool = demo_mode
        self.demo_male_count: int = 0

    def update_data(self):
        # Get first data call
        self.heartbeat_data = self.get_heartbeat_data(self.heartbeat_api_url)
        if self.demo_mode:
            self.heartbeat_data['data']['maleParticipants'] = self.heartbeat_data['data']['maleParticipants'] + self.demo_male_count
            self.heartbeat_data['data']['activeParticipants'] = self.heartbeat_data['data']['maleParticipants'] + self.heartbeat_data['data']['femaleParticipants']
            self.demo_male_count += 1000
        self.last_heartbeat_date = self.get_last_heartbeat_date(self.heartbeat_data)
        self.active_participant_count = self.get_active_participant_count(self.heartbeat_data)
        self.participant_demo_df = self.get_participant_demo_df(self.heartbeat_data)

    @staticmethod
    def get_heartbeat_data(url) -> dict:
        r = requests.get(url)
        return r.json() if r.ok else None

    @staticmethod
    def get_last_heartbeat_date(data) -> datetime.datetime:
        utc_txt = data.get('data').get('utc')
        time = datetime.datetime.strptime(utc_txt, '%H:%M:%S').time()
        date_time = datetime.datetime.combine(datetime.datetime.today(), time)
        return date_time if date_time else None

    @staticmethod
    def get_active_participant_count(data) -> int:
        ap_count = data.get('data').get('activeParticipants')
        return ap_count if ap_count else None

    @staticmethod
    def get_participant_demo_df(data) -> pd.DataFrame:
        d = data.get('data')
        d.pop('utc')
        d.pop('activeParticipants')
        d = {k.rstrip('Participants'): v for k, v in d.items()}
        df = pd.DataFrame(d.items(), columns=['Type', 'Value'])
        df.rename(columns={'Type': 'Sex', 'Value': 'Count'}, inplace=True)
        df.Sex = df.Sex.str.capitalize()
        return df

if __name__ == "__main__":

    my_ch = ConnectHeartbeat(demo_mode=True)

    print('Active participant count: {}'.format(my_ch.active_participant_count))
    print('Last heartbeat date: {}'.format(my_ch.last_heartbeat_date))
    print('Participant demo df: {}'.format(my_ch.participant_demo_df))

    my_ch.update_data()

    print('Active participant count: {}'.format(my_ch.active_participant_count))
    print('Last heartbeat date: {}'.format(my_ch.last_heartbeat_date))
    print('Participant demo df: {}'.format(my_ch.participant_demo_df))

    my_ch.update_data()

    print('Active participant count: {}'.format(my_ch.active_participant_count))
    print('Last heartbeat date: {}'.format(my_ch.last_heartbeat_date))
    print('Participant demo df: {}'.format(my_ch.participant_demo_df))

    my_ch.update_data()

    print('Active participant count: {}'.format(my_ch.active_participant_count))
    print('Last heartbeat date: {}'.format(my_ch.last_heartbeat_date))
    print('Participant demo df: {}'.format(my_ch.participant_demo_df))