import cx_Oracle
import matplotlib.pyplot as plt

print(cx_Oracle.version) #http://www.oracle.com/technetwork/articles/dsl/python-091105.html

con = cx_Oracle.connect('FUT_MTS/FUT_MTS@gdev-pk/MTS')
print(con.version)

cur = con.cursor()

l_sql = 'select row_number() over(order by t.ora_datetime) as x, ' \
        't.last as y ' \
        'from DAT_MQL_TICK t ' \
        'where t.id_symbol=3 and ' \
        "t.datetime between to_date('16.10.2017 10:00:00','dd.mm.yyyy hh24:mi:ss') and " \
                        " to_date('16.10.2017 11:00:00','dd.mm.yyyy hh24:mi:ss') " \
                                                                                ' order by t.ora_datetime'

cur.execute(l_sql)
lx=[]
ly=[]
for result in cur:
    #print(result)
    lx.append(result[0])
    ly.append(result[1])
cur.close()

print(min(ly)," ",max(ly))

plt.plot(lx, ly, 'b')
plt.axis([min(lx), max(lx), min(ly)-20, max(ly)+20])
plt.grid(True)
plt.show()

con.close()

f = open("test.csv", "w")
for i in range(len(lx)):
    f.write("{};{}\n".format(lx[i], ly[i]))
f.close()
