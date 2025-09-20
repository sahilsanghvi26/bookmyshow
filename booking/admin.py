from django.contrib import admin
from django.contrib import admin
from .models import Booking, Show, Seat, BookedSeat,City,Theatre,UserProfile,Movie

admin.site.register(City)
admin.site.register(UserProfile)
admin.site.register(Movie)
admin.site.register(Theatre)
admin.site.register(Show)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(BookedSeat)

