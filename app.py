import os
import csv
import subprocess


class App:
    def __init__(self, app_type:str, app_name:str, app_path:str, apps_csv_path:str):
        """ @param app_type type of the app, as illustrated above
                it can be 'term' or 'graphical';
            @param app_name app_name
            @param app_name app_name
            @param apps_csv_path the `apps.csv` file to remove/update the apps from/to
        """
        if not isinstance(app_type,str):
            raise TypeError("Wrong type for app_type in the constructor of class App");
        if not isinstance(app_name,str):
            raise TypeError("Wrong type for app_name in the constructor of class App");
        if not isinstance(app_path,str):
            raise TypeError("Wrong type for app_path in the constructor of class App");
        if not isinstance(apps_csv_path,str):
            raise TypeError("Wrong type for apps_csv_path in the constructor of class App");

        self.app_type = app_type
        self.app_name = app_name
        self.app_path = app_path
        self.apps_csv_path = apps_csv_path
        #print(f"New App with ({app_type=},{app_name=},{app_path=})")

    def register(self):
        """@param apps_csv_path the `apps.csv` file to add this app to.
        """
        if not os.path.isfile(self.apps_csv_path):
            print(f"Error: Register: '{self.apps_csv_path=}' does not exist")
            return False
        with open(self.apps_csv_path,"a",newline="") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            print("the app path is:",self.app_path)
            spamwriter.writerow([self.app_type,self.app_name,self.app_path])
            gen_text(self.apps_csv_path)


    def launch(self, launch_type_to_command, *args):
        command = launch_type_to_command.get(self.app_type,["sh","-c"])
        #print(command)
        command.append(f"{os.path.join(self.app_path,self.app_name)}{(' '+' '.join(args))if args else ''}")
        print("$ ",end="")
        for x in command:
            print(f"'{x}' ",end="")
        print('\b')
        subprocess.Popen(command)

    def delete(self):
        if not os.path.isfile(self.apps_csv_path):
            print(f"Error: Delete: '{self.apps_csv_path=}' does not exist")
            return False
        with open(self.apps_csv_path,"r",newline="") as csvfile:
            csv_lines = csvfile.readlines()

        with open(self.apps_csv_path,"w",newline="") as csvfile:
            spamwriter = csv.writer(csvfile,delimiter=',')
            found = False
            for line in csv_lines:
                if line.split(",")[1] == self.app_name:
                    found = True
                    break
            if found:
                for line in csv_lines:
                    if self.app_name != line.split(",")[1]:
                        spamwriter.writerow([x.strip() for x in line.split(",")])

        

    def check(self):
        if self.app_path is None or self.app_name is None:
            return False
        return os.path.isfile(os.path.join(self.app_path,self.app_name))

    @classmethod
    def update_all(cls, apps_csv_path):
        if not os.path.isfile(apps_csv_path):
            print(f"Error: Update: '{apps_csv_path=}' does not exist")
            return False
        with open(apps_csv_path,newline="") as csvfile:
            if os.stat(apps_csv_path).st_size != 0:
                spamreader = csv.reader(csvfile,delimiter=",")
                for type_, name, path in spamreader:
                    App(type_, name, path, apps_csv_path).update()
        gen_text(apps_csv_path)

    @classmethod
    def delete_all(cls, apps_csv_path):
        if not os.path.isfile(apps_csv_path):
            print(f"Error: Delete-All: '{apps_csv_path=}' does not exist")
            return False
        with open(apps_csv_path,"w",newline="") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow([])
            gen_text(apps_csv_path)

    def update(self):
        if not os.path.isfile(self.apps_csv_path):
            print(f"Error: Update: '{self.apps_csv_path=}' does not exist")
            return False

        elif self.check():
            # print("Updating ...")
            path_from = os.path.join(self.app_path,self.app_name)
            path_to = os.path.join(os.path.dirname(self.apps_csv_path),self.app_type,self.app_name)
            updated = False
            try:
                if os.path.isfile(path_to) and os.readlink(path_to) != path_from: # changed path
                    os.unlink(path_to)
                    updated = True
                os.symlink(path_from, path_to)
                gen_text(self.apps_csv_path)
                print(f"\033[32mLink '{path_to}'","created\033[m" if not updated else "updated\033[m");
            except FileExistsError:
                print(f"\033[33mLink '{path_to}' already exists.\033[0m");
            # TODO: Handle OSError case in try-catch
            # except OSError:


def die(msg):
    print(msg)
    exit(1)


def gen_text(csv_file):
    if not os.path.isfile(csv_file):
        raise FileExistsError(f"File does not exist: {csv_file}")

    dirname, basename = os.path.split(csv_file)
    if '.' in basename:
        basename = '.'.join(basename.split(".")[:-1])

    out = os.path.join(dirname,f'{basename}.ttext')

    print(f"Writing {out} from {csv_file}")
    with open(out,"w") as text:
        with open(csv_file,newline="") as csvfile:
            if os.stat(csv_file).st_size != 0:
                spamreader = csv.reader(csvfile,delimiter=",")
                for type_, name, path in spamreader:
                    text.write(os.path.join(type_,name)+"\n")
