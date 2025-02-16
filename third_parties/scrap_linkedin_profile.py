import os
import requests

from dotenv import load_dotenv

def scrap_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    load_dotenv()

    if mock:
        linkedin_profile_url = os.getenv("MOCK_LINKEDIN_URL")
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_key = os.getenv("PROXYCURL_API_KEY")
        headers = {"Authorization": "Bearer " + api_key}
        api_endpoint = os.getenv("PROXYCURL_API_ENDPOINT")
        params = {
            "linkedin_profile_url": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, headers=headers)

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }

    return data


if __name__ == "__main__":
    print(scrap_linkedin_profile(
        linkedin_profile_url="https://www.linkedin.com/in/lichengwang/"
    ))
