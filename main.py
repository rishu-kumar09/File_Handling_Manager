from pathlib import Path
import os

def creatingfile():
    try:
        name =input("Enetr your file name : ")
        path = Path(name)
        if not path.exists():
            with open(path,"w") as fs:
                data = input("what you want to write : ")
                fs.write(data)
            print("file creating successfully")
        else:
            print("Error file name is already exist")
    except Exception as err:
        print(f"an error occured as {err}")

def readingfile():
    try:
        name=input("please tell your file name :")
        path=Path(name)
        if path.exists():
            with open(path,"r") as fs:
               content = fs.read()
            print(f"your file content is \n{content}")
        else:
            print("error no such file exixsts")
    except Exception as err:
        print(f"sorry an error occured as {err}")

    
def updatingfile():
    try:
        name=input("Enter your file name : ")
        path=Path(name)
        if path.exists():
        
          print("Operation ")
          print("1. Renaming the file" )
          print("2. Appending the content")
          print("3. Overwriting the file")

        choice=int(input("Enter your option : "))

        if choice==1:
            newname=input("Enter your new file name : ")
            new_path=Path(newname)
            if not new_path.exists():
                path.rename(new_path)
                print("renamed succesfully")
            else:
                print("file  already exists")
        elif choice==2:
            with open(path,"a") as fs:
                data=input("what do you want to append : ")
                fs.write(" \n"+data)
                print("succesfully appended")
        elif choice==3:
                with open(path,"w") as fs:
                    data=input("what do you want to overwrite : ")
                    fs.write(" \n"+data)
                    print("succesfully overwritten")
    except Exception as err:
        print(f"sorry an error occured as {err}")
    

def deletingfile():
    try:
        name=input("Enter your file name :")
        path=Path(name)
        if path.exists():
            path.unlink()
            print("file deleted succesfully")
        else:
            print("error no such file exists")
    except Exception as err:
        print(f"sorry an error occured as {err}")
        



print("press 1 for creating file")
print("press 2 for reading file")
print("press 3 for updating file")
print("press 4 for deleting file")

a=int(input("\nEnter your responce : "))


if a==1:
    creatingfile()

if a==2:
    readingfile()

if a==3:
    updatingfile()

if a==4:
    deletingfile()