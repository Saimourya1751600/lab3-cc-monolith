from locust import task, FastHttpUser, between
from insert_product import login

class AddToCart(FastHttpUser):
    # Set a wait time between tasks to simulate real user behavior
    wait_time = between(1, 2)  # Adjust this as needed (1-2 seconds)

    def on_start(self):
        # Log in once and store the token for reuse
        self.username = "PES1UG22CS502"
        self.password = "PES1UG22CS502"
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")  # Save the token for reuse

    # Host URL
    host = "http://localhost:5000"

    # Define default headers to be used in requests
    default_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "application/json",  # Prefer JSON responses for easier parsing
    }

    @task
    def view_cart(self):
        # Send GET request to '/cart' with the token in the Authorization header
        headers = {
            **self.default_headers,  # Combine default headers with custom ones
            "Authorization": f"Bearer {self.token}"
        }
        response = self.client.get(
            "/cart",
            headers=headers
        )

        # Optional: Check if the response is successful (status code 200)
        if response.status_code != 200:
            self.environment.events.request_failure.fire(
                request_type="GET",
                name="/cart",
                response_time=response.elapsed.total_seconds() * 1000,  # in ms
                exception=f"Error: Response not OK, status code {response.status_code}",
            )

if __name__ == "__main__":
    from locust import run_single_user
    run_single_user(AddToCart)
