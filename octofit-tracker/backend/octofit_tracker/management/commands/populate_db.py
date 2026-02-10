from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        # Clear ManyToMany relationships before deleting teams
        for team in Team.objects.all():
            if team.pk:
                team.members.clear()
                team.delete()
        for user in User.objects.all():
            if user.pk:
                user.delete()

        # Create users (superheroes)
        marvel_users = [
            User(username='ironman', email='ironman@marvel.com', first_name='Tony', last_name='Stark'),
            User(username='captainamerica', email='cap@marvel.com', first_name='Steve', last_name='Rogers'),
            User(username='spiderman', email='spiderman@marvel.com', first_name='Peter', last_name='Parker'),
        ]
        dc_users = [
            User(username='batman', email='batman@dc.com', first_name='Bruce', last_name='Wayne'),
            User(username='superman', email='superman@dc.com', first_name='Clark', last_name='Kent'),
            User(username='wonderwoman', email='wonderwoman@dc.com', first_name='Diana', last_name='Prince'),
        ]
        for user in marvel_users + dc_users:
            user.save()

        # Create teams
        marvel_team = Team.objects.create(name='Team Marvel')
        marvel_team.members.set(marvel_users)
        dc_team = Team.objects.create(name='Team DC')
        dc_team.members.set(dc_users)

        # Create workouts
        workout1 = Workout.objects.create(name='Pushups', description='Do 20 pushups', difficulty='Easy', suggested_for='Beginners')
        workout2 = Workout.objects.create(name='Running', description='Run 5km', difficulty='Medium', suggested_for='Intermediate')
        workout3 = Workout.objects.create(name='Deadlift', description='Deadlift 100kg', difficulty='Hard', suggested_for='Advanced')

        # Create activities
        Activity.objects.create(user=marvel_users[0], activity_type='pushups', duration=10, calories_burned=50, date=timezone.now().date())
        Activity.objects.create(user=dc_users[0], activity_type='running', duration=30, calories_burned=300, date=timezone.now().date())
        Activity.objects.create(user=marvel_users[1], activity_type='deadlift', duration=20, calories_burned=200, date=timezone.now().date())

        # Create leaderboard
        Leaderboard.objects.create(user=marvel_users[0], score=150, rank=1)
        Leaderboard.objects.create(user=dc_users[0], score=120, rank=2)
        Leaderboard.objects.create(user=marvel_users[1], score=100, rank=3)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
