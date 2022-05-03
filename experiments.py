
def answer(ans):
    if ans.lower() == "category" or ans.lower() == "diagnosis":
        print("valid")
    else:
        err = {
            "status": "failed",
            "detail": "KeyError [use 'category' or 'diagnosis']",
        }
        print(err)


answer(ans='Categoy')
