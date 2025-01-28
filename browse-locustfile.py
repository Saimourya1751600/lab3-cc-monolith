from locust import task, run_single_user, between
from locust import FastHttpUser

class Browse(FastHttpUser):
    # Host URL
    host = "http://localhost:5000"

    # Essential default headers (removing unnecessary ones)
    default_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "application/json",  # Prefer JSON responses if possible
        "Connection": "keep-alive",   # Persistent connection (reuse for further requests)
        "DNT": "1",                    # Do Not Track header for privacy
    }

    # Wait time to simulate real user activity (customize as per needs)
    wait_time = between(1, 2)  # Wait between 1-2 seconds for better user simulation

    @task
    def browse_page(self):
        # Send GET request to '/browse' with optimized headers
        response = self.client.get(
            "/browse",
            headers=self.default_headers
        )
        
        # Optional: Check for response success (status code 200)
        if response.status_code != 200:
            self.environment.events.request_failure.fire(
                request_type="GET",
                name="/browse",
                response_time=response.elapsed.total_seconds() * 1000,  # in ms
                exception=f"Error: Response not OK, status code {response.status_code}",
            )

if __name__ == "__main__":
    run_single_user(Browse)
