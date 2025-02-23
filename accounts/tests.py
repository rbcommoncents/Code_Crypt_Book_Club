from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from accounts.models import CustomUser
from sitepages.models import Drink

class AdminTokenTestCase(TestCase):
    """Test case for verifying admin token authentication for creating and deleting a drink."""

    def setUp(self):
        """Set up an admin user and generate an API token."""
        self.client = APIClient()
        print("\n🔹 Setting up test environment...")

        # Create an admin user
        self.admin_user = CustomUser.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="securepassword"
        )
        print(f"Created admin user: {self.admin_user.email}")

        self.token, _ = Token.objects.get_or_create(user=self.admin_user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}
        print(f"🔑 Generated API Token: {self.token.key}")

    def test_create_and_delete_drink(self):
        """Test creating and deleting a drink using the admin API token."""
        print("\n🔹 Step 1: Creating a new drink...")

        # Step 1: Create a new drink
        create_response = self.client.post(
            "/api/drinks/",
            {
                "name": "Mocha",
                "category": "coffee",
                "ingredients": "Espresso, Steamed Milk, Chocolate Syrup, Whipped Cream",
                "method": "Combine espresso, steamed milk, and chocolate syrup. Stir well and top with whipped cream."
            },
            format="json",
            **self.auth_header  # Pass token authentication
        )

        if create_response.status_code == 201:
            print("Successfully created drink: Mocha")
        else:
            print(f"Failed to create drink! Response: {create_response.data}")

        self.assertEqual(create_response.status_code, 201, "Drink creation failed!")
        self.assertEqual(Drink.objects.count(), 1, "Drink was not added to the database.")

        drink_id = create_response.data["id"]
        print(f"🔹 Drink ID: {drink_id}")

        # Step 2: Retrieve the drink
        print("\n🔹 Step 2: Retrieving the drink details...")

        get_response = self.client.get(f"/api/drinks/{drink_id}/", **self.auth_header)

        if get_response.status_code == 200:
            print("Successfully retrieved drink details!")
        else:
            print(f"Failed to retrieve drink! Response: {get_response.data}")

        self.assertEqual(get_response.status_code, 200, "Failed to retrieve drink details.")
        self.assertEqual(get_response.data["name"], "Mocha", "Drink name mismatch!")

        # Step 3: Delete the drink
        print("\n🔹 Step 3: Deleting the drink...")

        delete_response = self.client.delete(f"/api/drinks/{drink_id}/", **self.auth_header)

        if delete_response.status_code == 204:
            print("Successfully deleted drink: Mocha")
        else:
            print(f"Failed to delete drink! Response: {delete_response.data}")

        self.assertEqual(delete_response.status_code, 204, "Drink deletion failed!")

        # Step 4: Ensure the drink is deleted
        print("\n🔹 Step 4: Verifying the drink is deleted...")

        self.assertEqual(Drink.objects.count(), 0, "Drink was not removed from the database.")
        print("Drink successfully removed from the database.")

if __name__ == "__main__":
    TestCase.main()
