from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    city_pincode = models.CharField(max_length=6)
    def __str__(self):
        return self.city_name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE )
    user_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.username

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=40)
    movie_language = models.CharField(max_length =15)
    movie_genre = models.CharField(max_length = 15)
    movie_release_date = models.DateField()
    movie_duration = models.PositiveIntegerField() 
    movie_grade = models.CharField(max_length=5)
    def __str__(self):
        return self.movie_name

class Theatre(models.Model):
    theatre_id = models.AutoField(primary_key=True)
    theatre_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    theatre_name = models.CharField(max_length=50)
    theatre_location = models.CharField(max_length=50)
    theatre_pincode = models.CharField(max_length=6)
    def __str__(self):
        return self.theatre_name

class Show(models.Model):
    show_id = models.AutoField(primary_key=True)
    show_timings = models.TimeField() 
    show_date = models.DateField()
    show_format = models.CharField(max_length=10)
    show_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="shows")
    show_theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="shows")

    def __str__(self):
        return f"{self.show_movie.movie_name} at {self.show_theatre.theatre_name} on {self.show_date} {self.show_timings.strftime('%I:%M %p')}"

class Seat(models.Model):
        seat_id = models.AutoField(primary_key=True)
        seat_row = models.CharField(max_length=5)
        seat_no = models.PositiveIntegerField()
        seat_type = models.CharField(max_length=10)
        seat_price = models.PositiveIntegerField()
        seat_theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name="seats")
        def __str__(self):
            return f"Seat {self.seat_row}{self.seat_no} ({self.seat_type}) in {self.seat_theatre.theatre_name}"

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateField()
    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
        ("CANCELLED", "Cancelled")
    ]
    booking_payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="PENDING")
    booking_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booking_show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="bookings")
    
    def __str__(self):
        return f"Booking {self.booking_id} by {self.booking_user.username} for {self.booking_show}"

class BookedSeat(models.Model):
    booked_seat_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booked_seats")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("seat", "show")

    def __str__(self):
        return f"{self.seat.seat_row}{self.seat.seat_no} for {self.show.show_movie.movie_name} ({self.show.show_date} {self.show.show_timings.strftime('%I:%M %p')})"

