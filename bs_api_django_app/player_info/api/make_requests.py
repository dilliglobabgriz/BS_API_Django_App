import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from typing import Dict, List, Any

class Api_Request:
    def __init__(self):
        self.method: str = 'get'
        self.BASE_URL: str = 'https://api.brawlstars.com/v1/'
        load_dotenv()
        self.API_KEY: str = os.getenv('BS_API_KEY')
        self.player_tag: str = ''
        self.endpoint: str = f'players/%23{self.player_tag}'

        self.headers: Dict[str, str] = {
          'Authorization': f'Bearer {self.API_KEY}',
           'Accept': 'application/json'
        }

    # Calls BS Api
    # Returns JSON object helper function
    def call_api(self, endpoint: str):
        response = requests.get(self.BASE_URL + endpoint, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
    
            return data
        else:
            raise Exception(f"Failed to retrieve data: {response.status_code}\n{response.text}")

    # Returns a JSON object
    def get_player_info(self) -> Dict[str, Any]:
        player_endpoint: str = self.get_player_info_endpoint()
        return self.call_api(player_endpoint)
    
    def get_global_rankings_info(self, top_n_players: int=10) -> List[Dict[str, Any]]:
        rankings_endpoint: str = f'rankings/global/players?limit={top_n_players}'
        rankings_data = self.call_api(rankings_endpoint)
        if rankings_data is None or 'items' not in rankings_data:
            raise Exception(f'Failed to fetch leaderboards top {top_n_players}')
        return rankings_data.get('items')
    
    def get_leaderboard_player_tags(self, top_n_players: int=10) -> List[str]:
        player_tags: List[str] = []
        rankings_data = self.get_global_rankings_info(top_n_players)
        for player in rankings_data:
            player_tags.append(player['tag'])
        return player_tags

    def get_general_brawler_info(self) -> List[Dict[str, Any]]:
        brawlers_endpoint: str = 'brawlers'
        brawlers_json = self.call_api(brawlers_endpoint)
        return brawlers_json.get('items')
        
    def get_all_brawlers_info(self) -> List[Dict[str, Any]]:
        player_data: Dict[str, Any] = self.get_player_info()
        return player_data.get('brawlers', [])
    
    def get_brawler_info(self, brawler_name: str) -> Dict[str, Any]:
        brawlers: List[Dict[str, Any]] = self.get_all_brawlers_info()
        for brawler in brawlers:
            if brawler.get('name') == brawler_name.upper():
                return brawler
            
        raise Exception(f"Could not find {brawler_name}")

    
    def get_player_info_endpoint(self) -> str:
        return f'players/%23{self.player_tag}'
    
    def set_endpoint(self, endpoint):
        self.endpoint = endpoint
        
    def set_player_tag(self, tag):
        self.player_tag = tag
        self.set_endpoint(tag)
    
    def get_player_tag(self) -> str:
        return self.player_tag
    
    def get_total_gears(self) -> int:
        gear_sum: int = 0
        brawlers: List[Dict[str, Any]] = self.get_all_brawlers_info()
        for brawler in brawlers:
            gear_sum += len(brawler.get('gears'))
        return gear_sum
    
    def get_total_star_powers(self) -> int:
        star_power_sum: int = 0
        brawlers: List[Dict[str, Any]] = self.get_all_brawlers_info()
        for brawler in brawlers:
            star_power_sum += len(brawler.get('starPowers'))
        return star_power_sum
    
    def get_total_gadgets(self) -> int:
        gadget_sum: int = 0
        brawlers: List[Dict[str, Any]] = self.get_all_brawlers_info()
        for brawler in brawlers:
            gadget_sum += len(brawler.get('gadgets'))
        return gadget_sum
    
    def get_total_brawlers(self) -> int:
        return len(self.get_general_brawler_info())
        
    
    def get_max_star_powers(self) -> int:
        star_power_total: int = self.get_total_brawlers() * 2
        return star_power_total
    
    # Currently exact same logic as max star powers
    # Seperate functions in case third star powers or gadgets are added
    def get_max_gadgets(self) -> int:
        gadget_total: int = self.get_total_brawlers() * 2
        return gadget_total
        
    def get_total_trophies(self) -> int:
        player_info = self.get_player_info()
        return player_info.get('trophies')

    # Could add name color as feature
    def get_gamer_tag(self) -> str:
        player_info = self.get_player_info()
        return player_info.get('name')
    
    def get_unlocked_brawlers(self) -> int:
        return len(self.get_all_brawlers_info())