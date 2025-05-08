import requests
import datetime

headers = {
    "X-RapidAPI-Key": "33a9b48d6fmsh163314ef6d9f9bcp1636f0jsnfd42903275f2",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def get_predictions():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    fixtures_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {"date": today}
    fixtures_response = requests.get(fixtures_url, headers=headers, params=params)
    fixtures = fixtures_response.json().get("response", [])

    def confidence(odd):
        if odd < 1.3:
            return 90
        elif odd < 1.4:
            return 80
        elif odd < 1.5:
            return 70
        return 0

    result = {"very_high": [], "high": [], "medium": []}

    for match in fixtures:
        try:
            fixture_id = match["fixture"]["id"]
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]

            odds_url = "https://api-football-v1.p.rapidapi.com/v3/odds"
            odds_params = {"fixture": fixture_id, "bookmaker": "6"}
            odds_response = requests.get(odds_url, headers=headers, params=odds_params)
            odds_data = odds_response.json().get("response", [])

            if not odds_data:
                continue

            odds_values = odds_data[0]["bookmakers"][0]["bets"][0]["values"]
            odds_dict = {item["value"]: float(item["odd"]) for item in odds_values}

            for side in ["Home", "Away"]:
                if side in odds_dict:
                    conf = confidence(odds_dict[side])
                    if conf >= 70:
                        prediction = {
                            "match": f"{home} vs {away}",
                            "prediction": f"{home if side == 'Home' else away} to WIN",
                            "confidence": f"{conf}%",
                            "odds": str(odds_dict[side])
                        }
                        if conf == 90:
                            result["very_high"].append(prediction)
                        elif conf == 80:
                            result["high"].append(prediction)
                        elif conf == 70:
                            result["medium"].append(prediction)
                    break
        except Exception:
            continue

    return {
        "status": "success",
        "date": today,
        "predictions": result
    }
