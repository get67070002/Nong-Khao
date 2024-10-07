"""Find da free"""
def btsmrt (day,age,height) :
    """free free free"""
    if day == "Senior Day" and age >= 60 :
        print("FREE")
    elif day == "Children Day" and age < 14 and height <= 140 :
        print("FREE")
    elif age < 14 and height < 90 :
        print("FREE")
    else :
        print("PAY")
btsmrt(input(),float(input()),float(input()))
