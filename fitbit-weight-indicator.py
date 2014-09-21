import pygtk
pygtk.require('2.0')
import gtk
import appindicator
import gobject
import fitbit
import json
import io

class FitbitIndicator:
  def __init__(self):
    self.ind = appindicator.Indicator ("Fitbit Weight Indicator", "indicator-messages", appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    self.ind.set_icon("stock_right")
    self.ind.set_label("...") 

    # create a menu
    self.menu = gtk.Menu()

    image = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    image.connect("activate", self.quit)
    image.show()
    self.menu.append(image)
               
    self.menu.show()
    self.menu2 = self.menu

    self.ind.set_menu(self.menu)

    # load config
    self.conf = {}
    with io.open('config.json', 'r', encoding='utf-8') as f:
      self.conf = json.load(f)

    # init fitbit
    self.fitbit = fitbit.Fitbit(self.conf['FitbitConsumerKey'], self.conf['FitbitConsumerSecret'], resource_owner_key=self.conf['FitbitUserKey'], resource_owner_secret=self.conf['FitbitUserSecret'], system='de_DE')
    # FIXME: Check if login successfull
   
    self.getFitbitData()
    gobject.timeout_add(30 * 1000, self.getFitbitData)

  def quit(self, widget, data=None):
    gtk.main_quit()

  def getFitbitData(self):
    try:
      weightlog = self.fitbit.get_bodyweight(period='1m')
    except:
      return 1

    weightdiff = weightlog['weight'][-1]['weight'] - weightlog['weight'][-2]['weight']
    weight = weightlog['weight'][-1]['weight']
    bmi = weightlog['weight'][-1]['bmi']

    if weightdiff > 0:
      self.ind.set_icon("up")
    elif weightdiff < 0:
      self.ind.set_icon("down")
    else:
      self.ind.set_icon("stock_right")

    self.ind.set_label(str(weight) + " " + str(weightdiff) + " " + str(bmi))

    return 1

def main():
  gtk.main()
  return 0

if __name__ == "__main__":
  indicator = FitbitIndicator()
  main()
