"""
parse_agent.py is a real-time parser to parse the mosquitto broker log for flow control

By default the log file is stored in directory '/home/shangxing/iot_log/test.log'
"""

import re
import time
import MySQLdb
import datetime
import pytz
from ConfigParser import SafeConfigParser
import os 

DEBUG = 1

def process(line, flows_list, sub_dict, pub_dict, pub_topic_dict, sub_topic_dict, sub_topic_dict_init):
    """Process one line of strings in the log file

    Args:
        line (str): one line of strings from the log
        sub_dict (dict): a dictionary to maintain subscribers' info.
                        key=subscriber's name, value=True if subscribing currently, else false
        pub_dict (dict): a dictionary to maintain publishers' info.
                        key=publisher's name, value=True if publishing currently, else false
        sub_topic_dict (dict): a dictionary mapping from (subscriber, topic) to ordered num of messages

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
            
            #get all flows that have this flow
            got_one = False
            for item in flows_list:
                if item['flow'] == f:
                    got_one = True
                    item['cur_n_items'] += 1
                    item['update'] = True           
                    if DEBUG:
                        print 'New message to ' + str(f[:-1])
                        
            if got_one == False:
                # TO-DO, figure out what is the best way to set the n_items_sub 
                # (number of items subscribed)
                flows_list.append({'flow': f,
                                   'cur_n_items': 1,
                                   'init_n_items': 1,
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
                    item['update'] = True
                    if DEBUG:
                        print 'New message from ' + str(f[:-1])
                    
            if got_one == False:
                flows_list.append({'flow': f,
                                   'cur_n_items': 1,
                                   'init_n_items': 0,
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
                    item['cur_n_items'] = 0
                    item['init_n_items'] = int(words[4])
                    item['update'] = True
            
            if got_one == False:
                flows_list.append({'flow': f,
                                   'cur_n_items': 0,
                                   'init_n_items': int(words[4]),
                                   'connected': True,
                                   'update': True})
            if DEBUG:
                print 'New subscribed flow ' + str(f[:-1])
                        
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
    sub_dict = {}               # Subscribers
    pub_dict = {}               # Publishers
    sub_topic_dict = {}         # Current subscribers
    pub_topic_dict = {}         # Current publishers
    sub_topic_dict_init = {}    # Initial subscriber values
    
    #read config file
    config = SafeConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read('/code/config.ini')
    path = config.get('main', 'log_path')

    #DB connections
    mysql_con = MySQLdb.connect(host=config.get('main', 'mysql_host'),
                    user=config.get('main', 'mysql_name'),
                    passwd=config.get('main', 'mysql_pw'),
                    db=config.get('main', 'mysql_db'))
    mysql_cur = mysql_con.cursor()

    #log file
    logfile = open(path, "r")
    loglines = follow(logfile)

    for line in loglines:

        process(line, flows_list, sub_dict, pub_dict, pub_topic_dict, sub_topic_dict, sub_topic_dict_init)
        print_list = False
        #check if any flow has been changed
        for item in flows_list[:]:
            if item['update'] == False:
                continue
                       
            #get user and product id
            user = str(item['flow'][0])
            topic = str(item['flow'][1])
            try:
                test_select = mysql_cur.execute("select * from auth_user")
                print user
                user_id = mysql_cur.execute("select id from auth_user where username = %s", (user,))
                user_id = mysql_cur.fetchone()
                user_id = user_id[0]
                product_id = mysql_cur.execute("select id from products_product where title = %s", (topic, ))
                product_id = mysql_cur.fetchone()
                product_id = product_id[0]
            except:
                print 'Not able to retrieve user_id and product_id' + str((user, topic))
                continue
            #subscribers
            if item['flow'][2] == 'out':
                remaining_items = item['init_n_items'] - item['cur_n_items']
                
                #insert into item_count table
                if remaining_items == item['init_n_items']:
                    mysql_cur.execute('update billing_itemcount set quantity = %s where buyer_id = %s and product_id = %s and success = %s',
                                   (remaining_items, user_id, product_id, 0))
                else:
                    date = datetime.datetime.now(pytz.UTC)
                    mysql_cur.execute('update billing_itemcount set quantity = %s, last_recv_timestamp = %s where buyer_id = %s and product_id = %s and success = %s',
                                   (remaining_items, date, user_id, product_id, 0))
                
                if remaining_items > 0 and remaining_items != item['init_n_items']:
                    mysql_cur.execute('update flows_flow set state = %s where user_id = %s and direction = %s and topic = %s',
                                       ('subscribing', user_id, 'in', topic))
                elif remaining_items == 0:
                    mysql_cur.execute('update billing_itemcount set success = %s where buyer_id = %s and product_id = %s and success = %s',
                                       (1, user_id, product_id, 0))
                    mysql_cur.execute('update flows_flow set state = %s where user_id = %s and direction = %s and topic = %s',
                                       ('done', user_id, 'in', topic))
                    
                    mysql_cur.execute("delete from acls where username= %s and topic = %s", (user, topic))

                    #removing the item that does not have anymore data to receive
                    flows_list.remove(item)

                    mysql_con.commit()

            #publishers
            elif item['flow'][2] == 'in':
                print item['flow']
                mysql_cur.execute('update flows_flow set state = %s where user_id = %s and direction = %s and topic = %s',
                                   ('publishing', user_id, 'out', topic))
                mysql_con.commit()
                
            #check if the node was disconnected
            if item['connected'] == False:
                mysql_cur.execute('update flows_flow set state = %s where user_id = %s',('inactive', user_id))
                mysql_con.commit()
                
                flows_list.remove(item)

            #set the update back to False
            item['update'] = False
            
            #print list
            print_list = True
        
        if print_list == True:
            print flows_list
        