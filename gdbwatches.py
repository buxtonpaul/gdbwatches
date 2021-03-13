#  Copyright Paul Buxton 2021
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import gdb

""" GDB extension to add a watch window and a locals window to gdb using TUI """

localwin = None
watchwin = None
watches=[]


class localWinClass():
  """ Locals window displays the current locals"""
  def __init__(self, parent):
    global localwin
    localwin = self
    self.outwin = parent
    self.outwin.title = "Locals"
    gdb.events.cont.connect(self.listener)

  def render(self):
    locals = gdb.execute("info locals", to_string=True)
    self.outwin.erase()
    self.outwin.write(locals)

  def listener(self, event):
    self.render()

  def close(self):
    global localwin
    localwin=None
    gdb.events.cont.disconnect(self.listener)


class addWatch(gdb.Command):
  """ add an expression to watch"""
  def __init__(self):
    super(addWatch, self).__init__("addwatch",gdb.COMMAND_USER)

  def invoke (self, expression,from_tty):
    global watches
    watches.append(expression)
    watchwin.render()





class removeWatch(gdb.Command):
  """ remove a watched expression takes an index number to the list"""
  def __init__ (self):
    super (removeWatch, self).__init__ ("removewatch",gdb.COMMAND_USER)

  def invoke (self, variable,from_tty):
    if int(variable) < len(watches):
      watches.pop(int(variable))
      watchwin.render()
    else:
      print ("Index {} doesnt exist".format(variable))


class watchWinClass():
  """ Window to watch expressions """
  def __init__(self,parent):
    global watchwin 
    watchwin = self
    self.outwin=parent
    self.outwin.title= "Watches"
    gdb.events.cont.connect(self.listener)
    addWatch()
    removeWatch()

  def render(self):
    global watches
    self.outwin.erase()
    index=0
    for a in watches:
      try :
        val = str(gdb.parse_and_eval(a))
      except:
        val="??"
      outstring = "{} : {}  = {}\n\n".format(index,a,val)
      self.outwin.write(outstring)
      index+=1

  def listener(self,event):
    self.render()

  def close(self):
    global watchwin
    watchwin=None
    gdb.events.cont.disconnect(self.listener)

gdb.register_window_type("locals",localWinClass)
gdb.register_window_type("watches",watchWinClass)
gdb.execute("tui new-layout watchvars {-horizontal src 20 {locals 1 watches 1} 5} 40 status 0 cmd 1")
gdb.execute("layout watchvars")
