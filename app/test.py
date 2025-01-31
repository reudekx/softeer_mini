import json
import os
from pathlib import Path
from app.core.extractor import Site, extract

def ensure_directories():
    """필요한 디렉토리들을 생성합니다."""
    directories = [
        'data/fbref/json',
        'data/fotmob/json'
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def save_json(data, site_dir, player_name):
    """JSON 데이터를 파일로 저장합니다."""
    filepath = Path(f'data/{site_dir}/json/{player_name}.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {filepath}")

def test_players():
    # 디렉토리 생성
    ensure_directories()
    
    # players.json 파일 로드
    with open('app/players.json', 'r', encoding='utf-8') as f:
        players = json.load(f)
    
    # 각 선수에 대해 데이터 추출 및 저장
    for player in players:
        print(f"\nProcessing {player['name']}...")
        
        try:
            # Fotmob 데이터 추출 및 저장
            fotmob_data = extract(
                site=Site.FOTMOB,
                url=player['fotmob_url'],
                name=player['name']
            )
            save_json(fotmob_data, 'fotmob', player['name'])
            
            # FBref 데이터 추출 및 저장
            fbref_data = extract(
                site=Site.FBREF,
                url=player['fbref_url'],
                name=player['name']
            )
            save_json(fbref_data, 'fbref', player['name'])
            
        except Exception as e:
            print(f"Error processing {player['name']}: {str(e)}")
            raise e

if __name__ == "__main__":
    test_players()