from django.shortcuts import render
import hashlib
import requests

def index(request):
    context = {}
    if request.method == "POST":
       inputbox = request.POST.get('input',)
       
       if inputbox is not None:
         enc = hashlib.sha1(inputbox.encode())
         hexa = enc.hexdigest()
         hexa = hexa.upper()
       
       try:
         #check beginning of string
         url = f'https://api.pwnedpasswords.com/range/{hexa[:5]}'
         response = requests.get(url)
         data = response.text
         response.raise_for_status()
         
         lines = data.split('\n')
         total = 0
         #get total breach
         for line in lines:
             split = line.split(":")
             total += int(split[1])
              
         #check rest of string
         if hexa[5:] in data:
             context['pwnedornot'] = "You have been pwned!"
             context['breachnum'] = f"Your password appears a total of {total} times in breached data!\nYou should consider changing your password."
         else:
             context['pwnedornot'] = f"You have not been pwned\n\n"
             
       except requests.exceptions.RequestException as e:
               context['pwnedornot'] = f"{e}"

       context['inputbox'] = "Checking for password: "+inputbox

    return render(request, 'myapp/index.html',context)
