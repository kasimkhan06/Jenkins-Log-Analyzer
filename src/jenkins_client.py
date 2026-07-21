from dotenv import load_dotenv
from pydantic import BaseModel , Field
import requests
import os
load_dotenv()

class JenkinsURL(BaseModel):

    job_base_url : str = Field(
        description = 'Base url of the jenkins job',
    )
    job_name : str = Field(
        description='Name of the Job'
    )
    job_number : str = Field(
        description='Number of the job executed'
    )

def parse_jenkins(url : str) -> JenkinsURL :

    """
        Returns the job_path and build_number when passed an entire Jenkins URL
    """
    url = url.rstrip('/')
    job_base_url = url.split('/')[0] + "//" + url.split('/')[2]
    job_name = '/'.join(url.split('job/', 1)[1].split('/')[:-1])
    job_number = url.split('job/', 1)[1].split('/')[-1]

    jenkins_info = JenkinsURL(
        job_base_url= job_base_url,
        job_name=job_name,
        job_number=job_number
    )

    return jenkins_info

def get_build_status(jenkins_info: JenkinsURL) -> dict:
    """
    Fetches build metadata (result, building status, etc.) from Jenkins.
    Raises ValueError on bad auth, missing build, or unreachable server.
    """
    url = f"{jenkins_info.job_base_url}/job/{jenkins_info.job_name}/{jenkins_info.job_number}/api/json"
    print(url)
    response = requests.get(
        url,
        auth=(os.getenv("JENKINS_USER"), os.getenv("JENKINS_API_TOKEN")),
        verify="/home/kkhan3/ZscalerRootCertificate-2048-SHA256.pem",
        timeout=10,
    )

    if response.status_code == 401:
        raise ValueError("Jenkins authentication failed — check JENKINS_USER/JENKINS_API_TOKEN")
    if response.status_code == 404:
        raise ValueError(f"Build not found: {url}")
    if response.status_code != 200:
        raise ValueError(f"Unexpected Jenkins response ({response.status_code}) for {url}")

    data = response.json()

    return {
        "result": data.get("result"),
        "building": data.get("building"),
        "timestamp": data.get("timestamp"),
    }


if __name__ == "__main__":

    info = parse_jenkins(url = "http://chipd007.chennai.visteon.com:9090/job/Ford_Phoenix_ACM_CI_Integration/385/")
    print(info)
    status = get_build_status(info)
    print(status)