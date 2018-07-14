import pandas as pd
import sys, urllib3
import requests
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets

class PokeDex(QtWidgets.QWidget):

    def __init__(self):
        super(PokeDex, self).__init__()

        self.initUI()

    def initUI(self):
        # Initial UI
        
        # Grid Layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        # Parse JSON from DataFrame
        self.df = pd.read_json('PokemonData.json')
        self.df = self.df.set_index(['#'])

        # Drop Down
        self.dropdown = QtWidgets.QComboBox(self)
        self.names = self.df['Name'].values
        self.dropdown.addItems(self.names)
        self.grid.addWidget(self.dropdown, 0,0,1,1)

        # Search Button
        self.btn = QtWidgets.QPushButton('Search', self)
        self.btn.clicked.connect(self.runSearch)
        self.grid.addWidget(self.btn, 0,1,1,1)

        # Image
        self.img = QtWidgets.QLabel(self)
        self.grid.addWidget(self.img, 1,1,1,1)

        # Stats
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText('\nName:\n\nType:\n\nHP:\n\nAttack:\n\nSp. Attack\n\nDefense:\n\nSp. Defense\n\nSpeed:\n\nTotal:')
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.label, 1,0,1,1)

        # Customize Widgets
        self.resize(500, 250)
        self.center()
        self.setWindowTitle('PokeDex')
        self.show()

    def runSearch(self):
        # Event for run button

        # Parse values
        index = self.dropdown.currentIndex()
        val = self.names[index]
        cond = self.df['Name'] == val

        # Image
        http = urllib3.PoolManager()
        base = 'https://img.pokemondb.net/artwork/'
        img_url = base + val.lower() + '.jpg'
        response = http.request('GET', img_url)
        data = response.data
        #data = urllib3.urlopen(img_url).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self.img.setPixmap(QtGui.QPixmap(image))

        # Set Values
        name = 'Name:\t\t\t' + val + '\n\n'
        ty = 'Type:\t\t\t' + ', '.join(self.df[cond]['Type'].values[0])+'\n\n'
        hp = 'HP:\t\t\t' + str(self.df[cond]['HP'].values[0])+'\n\n'
        atk = 'Attack:\t\t\t' + str(self.df[cond]['Attack'].values[0])+'\n\n'
        satk = 'Sp. Attack:\t\t' + str(self.df[cond]['Sp. Atk'].values[0])+'\n\n'
        deff = 'Defense:\t\t' + str(self.df[cond]['Defense'].values[0])+'\n\n'
        sdef = 'Sp. Defense:\t\t' + str(self.df[cond]['Sp. Def'].values[0])+'\n\n'
        speed = 'Speed:\t\t\t' + str(self.df[cond]['Speed'].values[0])+'\n\n'
        total = 'Total:\t\t\t' + str(self.df[cond]['Total'].values[0])+'\n\n'

        # Add text
        final = name+ty+hp+atk+satk+deff+sdef+speed+total
        self.label.setText(final)

    def center(self):
        # Center on screen
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():

    # Create app object to run QT
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)

    # QT GO!!
    gui = PokeDex()
    # Exit cleanly
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
