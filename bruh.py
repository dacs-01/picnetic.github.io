ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


filename = "HI.txt"
bruh  ="j.html"
hi = "asdfadsf.pdf"
hihih = "hihihihhihihi.jpeg"
hihihihhihih = "hi.hi.jpg"


arr = [filename, bruh, hi, hihih, hihihihhihih]

for i in arr:
    g = i.split('.')

    if g[-1].lower() in ALLOWED_EXTENSIONS:
        print(i + " GOOD")
    else:
        print(i + " BAD")
    