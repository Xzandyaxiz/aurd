import subprocess, sys, os

class AUR:
    def __init__(self):
        self.packages_info = []
        self.package_dict = {}

    def search(self, s):
        output = subprocess.check_output(['curl', f'https://aur.archlinux.org/packages?O=0&SeB=nd&K={s}&outdated=&SB=p&SO=d&PP=250&submit=Go'])
        self.parse(output.decode())

    def parse(self, s):
        name = ""
        desc = ""

        print('\033c', end='', flush=True)

        rows = s.split('\n')
        
        for index, row in enumerate(rows):
            if '<tr>' in row:
                self.packages_info.append(rows[index:index+18])

        for package_info in self.packages_info:
            for package in package_info:
                line = package.strip()

                if '/packages/' in package:
                    name = line[19:-2]

                elif '"wrap"' in package:
                    desc = line[17:-5]

                self.package_dict[f'{name}'] = { "desc": desc }

    def install(self):
        for index, pkg in enumerate(self.package_dict):
            print(str(index) + " " + f"aur/{pkg}" + "\n    " + self.package_dict[pkg]["desc"])

        print(":: Insert packages (e.g 1 2 3)")
        inp = input(":: ")

        pkg_split = inp.split(' ')
        packages = [package for package in self.package_dict]

        for pkg in pkg_split:
            if not pkg.isdigit():
                continue

            package = packages[int(pkg)]

            link = f"https://aur.archlinux.org/{package}.git"

            os.system(f'git clone {link}')
            os.system(f'(cd {package} && makepkg PKGBUILD)')
            os.system(f'rm -rf {package}')

if __name__ == "__main__":    
    aur = AUR()

    aur.search(sys.argv[1])
    aur.install()