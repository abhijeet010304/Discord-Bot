import matplotlib.pyplot as plt
import numpy as np
#get userdata of contest and build all pie graphs
def pie_plot(alldata,index,user):
    subject=[]
    perc = []
    total = 0
    explode = []
    finallist=[]

    for value in alldata[index]:
        total+=alldata[index][value]
        explode.append(0)
        subject.append(value)

    explode[2] = 0.1
    for value in alldata[index]:
        percentage = alldata[index][value]
        percentage *= 100;
        percentage /=total
        finallist.append(value+':'+str(round(percentage,2))+'%')
        perc.append(percentage)
    #form graph used belw info from StackOF
    fig, ax = plt.subplots(figsize=(11, 6), subplot_kw=dict(aspect="equal"))


    data = perc
    recipe = finallist

    wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=50)

    bbox_props = dict(boxstyle="square,pad=0.1", fc="w", ec="k", lw=1.2)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(recipe[i], xy=(x, y), xytext=(1.3*np.sign(x), 1.5*y),
                    horizontalalignment=horizontalalignment, **kw)
    plt.legend(finallist,loc="center left", bbox_to_anchor=(-0.5, 0.5))
    graph_type = 'Verdict'
    if index == 0:
        graph_type = 'Programming-Language'
    elif index == 1:
        graph_type = 'level'
    elif index == 2:
        graph_type = 'Problem-Level'
    elif index == 3:
        graph_type = 'Problem-Tags'
    else :
        graph_type = 'Verdict'

    ax.set_title(graph_type + ' Graph of : '  + user)
    return ax
    # plt.show()

#get userdata of contest and build rating graph
def rating_plot(data1,data2,user1,user2):
    x1 = []
    y1 = []

    x2 = []
    y2 = []
    # print(data1)
    for a in data1:
        x1.append(a[0])
        y1.append(a[1])
    for a in data2:
        x2.append(a[0])
        y2.append(a[1])
    # date_form = DateFormatter("%m-%d")
    ax =plt.plot(x1, y1, label = user1)
    ax = plt.plot(x2, y2, label = user2)
    plt.xlabel('month-year ')
    plt.ylabel('Ratings')
    plt.legend()
    return ax
    # plt.show()
