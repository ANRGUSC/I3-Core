"""
parse_agent.py is a real-time parser to parse the mosquitto broker log for flow control

By default the log file is stored in directory '/home/shangxing/iot_log/test.log'
"""

import re
import time
import MySQLdb
import sqlite3
import datetime
import pytz
from ConfigParser import SafeConfigParser

# billing types used
PER_ITEM = 1
PER_DAY = 2

DEBUG = 1

def process(line, flows_list):
    """Process one line of strings in the log file

    Args:
        line (str): one line of strings from the log
        flows_list (list): a list with all flows information.

    Returns:

    """
    words = filter(None, re.split("[, \-!?:() \n]+", line))
    words = words[1:]
    if len(words) > 2:
        #TO DO: 1. denied published
        #       2. how to tell when someone stops publishing/subscribing
        
        #sending a confirmation to a sub
        if words[0] == 'Sending' and words[1] == 'SUBACK':
            pass

        #sending message to sub
        elif words[0] == 'Sending' and words[1] == 'PUBLISH':
            user = words[3]
            topic = words[-4][1:-1]
            dir = 'out'
            f = (user, topic, dir)
            
            #get all entries that have this flow
            got_one = False
            for item in flows_list:
                if item['flow'] == f:
                    got_one = True
                    item['cur_n_items'] += 1
                    item['cur_datetime'] = datetime.datetime.now(pytz.UTC)
                    item['update'] = True           
                    if DEBUG:
                        print 'New message to ' + str(f[:-1])
                        
            if got_one == False:
                flows_list.append({'flow': f,
                                   'cur_n_items': 1,
                                   'init_n_items': 1,
                                   'cur_datetime': datetime.datetime.now(pytz.UTC),
                                   'init_datetime': datetime.datetime.now(pytz.UTC),
                                   'connected': True,
                                   'update': True})
                if DEBUG:
                    print 'New flow ' + str(f)
                    print 'New message to ' + str(f[:-1])

        #receive message from pub
        elif words[0] == 'Received' and words[1] == 'PUBLISH':
            user = words[3]
            topic = words[-4][1:-1]
            dir = 'in'
            f = (user, topic, dir)
                        
            #get all flows that have this flow
            got_one = False
            for item in flows_list:
                if item['flow'] == f:
                    got_one = True
                    item['cur_n_items'] += 1
                    item['cur_datetime'] = datetime.datetime.now(pytz.UTC)
                    item['update'] = True
                    if DEBUG:
                        print 'New message from ' + str(f[:-1])
                    
            if got_one == False:
                flows_list.append({'flow': f,
                                   'cur_n_items': 1,
                                   'init_n_items': 0,
                                   'cur_datetime': datetime.datetime.now(pytz.UTC),
                                   'init_datetime': datetime.datetime.now(pytz.UTC),
                                   'connected': True,
                                   'update': True})
                if DEBUG:
                    print 'New flow ' + str(f)
                    print 'New message from ' + str(f[:-1])
                    
        #receive disconnection from a node
        elif words[2] == 'disconnected.':
            user = words[1]
            
            for item in flows_list:
                if item['flow'][0] == user:
                    item['connected'] = False
                    item['update'] = True
                    if DEBUG:
                        print 'User ' + user + ' disconnected'
                        
        #receive connection error from a node
        elif words[0] == 'Socket' and words[1] == 'error':
            user = words[-2]

            for item in flows_list:
                if item['flow'][0] == user:
                    item['connected'] = False
                    item['update'] = True
                    if DEBUG:
                        print 'User ' + user + ' error'
                        
        #receive ordered num of messages from a sub for a topic
        elif words[0] == 'New' and words[1] == 'Sub':
            user = words[2]
            topic = words[3]
            dir = 'out'
            f = (user, topic, dir)
            
            got_one = False
            for item in flows_list:
                if item['flow'] == f:
                    got_one = True
                    item['init_n_items'] += int(words[4])
                    item['init_datetime'] = datetime.datetime.now(pytz.UTC)
                    item['update'] = True
            
            if got_one == False:
                flows_list.append({'flow': f,
                                   'cur_n_items': 0,
                                   'init_n_items': int(words[4]),
                                   'cur_datetime': datetime.datetime.now(pytz.UTC),
                                   'init_datetime': datetime.datetime.now(pytz.UTC),
                                   'connected': True,
                                   'update': True})
            if DEBUG:
                print 'New subscription of ' + words[4] + ' items from flow ' + str(f[:-1])
                        
        else:
            pass


def follow(thefile):
    """Read a new line from the log file

    Args:
        thefile: log file reference

    Returns:
        line: a new line
    """
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':

    flows_list = []
    # this is a list with the main information for the parser
    # each entry is composed of:
    # 'flow' : tuple (user, topic, direction), where direction is 'out' if buyer and 'in' if seller
    # 'cur_n_items' : current number of items on this flow. if buyer, # of items bought, if seller, # of items published
    # 'init_n_items' : initia number of items bought. just makes sense for buyer
    # 'update' : flag that says that something has changed and the DB has to be updated
    # 'connected' : flag that says that the user is currently connected
    
    #read config file
    config = SafeConfigParser()
    config.read('/usr/local/iotm/config.ini')
    path = config.get('main', 'log_path')

    #log file
    logfile = open(path, "r")
    loglines = follow(logfile)

    for line in loglines:
        process(line, flows_list)

        print_list = False
        
        #check if any flow has been changed
        for item in flows_list[:]:
            if item['update'] == False:
                continue
                       
            #DB connections
            mysql_con = MySQLdb.connect(host="localhost",
                        user=config.get('main', 'mysql_name'),
                        passwd=config.get('main', 'mysql_pw'),
                        db=config.get('main', 'mysql_db'))
            mysql_cur = mysql_con.cursor()
    
            #get user and product id
            user = item['flow'][0]
            topic = item['flow'][1]
            print user
            try:
                mysql_cur.execute("select id from auth_user where username = %s", (user,))
                (user_id,) = mysql_cur.fetchone()
                mysql_cur.execute("select id from products_product where title = %s", (topic, ))
                (product_id, ) = mysql_cur.fetchone()
            except:
                print 'Not able to retrieve user_id and product_id' + str((user, topic))
                continue
                
            #subscribers
            if item['flow'][2] == 'out':
                mysql_cur.execute("select billing_type from billing_itemcount where buyer_id = %s and product_id = %s and success = %s", (user_id, product_id, 0 ))
                (billing_type, ) = mysql_cur.fetchone()

                if billing_type == PER_ITEM:
                    remaining_items = item['init_n_items'] - item['cur_n_items']
                    print "-- Per item billing"
                elif billing_type == PER_DAY:
                    remaining_items = item['init_n_items'] - (item['cur_datetime'] - item['init_datetime']).days
                    if remaining_items < 0:
                        remaining_items = 0
                    print "-- Per day billing"

                print "-- Remaining: " + str(remaining_items)

                #insert into item_count table
                if remaining_items == item['init_n_items']:
                    mysql_cur.execute('update billing_itemcount set quantity = %s where buyer_id = %s and product_id = %s and success = %s', (remaining_items, user_id, product_id, 0))
                else:
                    #date = datetime.datetime.now(pytz.UTC)
                    mysql_cur.execute('update billing_itemcount set quantity = %s, last_recv_timestamp = %s where buyer_id = %s and product_id = %s and success = %s', (remaining_items, item['cur_datetime'], user_id, product_id, 0))
                    
                if remaining_items > 0 and remaining_items != item['init_n_items']:
                    mysql_cur.execute('update flows_flow set state = %s where user_id = %s and direction = %s and topic = %s', ('subscribing', user_id, 'in', topic))
                elif remaining_items == 0:
                    mysql_cur.execute('update billing_itemcount set success = %s where buyer_id = %s and product_id = %s and success = %s', (1, user_id, product_id, 0))
                    mysql_cur.execute('update flows_flow set state = %s where user_id = %s and direction = %s and topic = %s', ('done', user_id, 'in', topic))
                    mysql_cur.execute("delete from acls where username= %s and topic = %s", (user, topic))
                    
                    #removing the item that does not have anymore data to receive
                    flows_list.remove(item)
                    
            #publishers
            elif item['flow'][2] == 'in':
                mysql_cur.execute('update flows_flow set state = %s where user_id = %s and direction = %s and topic = %s', ('publishing', user_id, 'out', topic))
                
            #check if the node was disconnected
            if item['connected'] == False:
                mysql_cur.execute('update flows_flow set state = %s where user_id = %s',('inactive', user_id))
                
                #if it is a buyer that received all data we can remove from flows_list
                if item['flow'][2] == 'out' and item['init_n_items'] == item['cur_n_items']:
                    flows_list.remove(item)

            #set the update back to False
            item['update'] = False
            
            #commit changes and close
            mysql_con.commit()
            mysql_con.close()
            
            #print list
            print_list = True
        
        if print_list == True:
            print flows_list
        
