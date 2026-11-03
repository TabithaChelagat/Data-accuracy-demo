"""Cleans data/branch_sales.csv with the same rules the web page uses, prints the margin bridge, and writes output/ files."""
import csv, re
rd=lambda f:list(csv.DictReader(open("data/"+f)))
M={r["code"]:dict(name=r["name"],cat=r["category"],price=float(r["shelf_price"]),erp=float(r["erp_cost"]),ml=float(r["size_ml"])) for r in rd("item_master.csv")}
for r in rd("supplier_costs.csv"): M[r["code"]]["sup"]=float(r["supplier_cost"])
KEY={r["line_id"]:r for r in rd("answer_key.csv")}
def norm(c):
    d="".join(re.findall(r"\d+",c)); return "NV-"+d if d else None
rnd=lambda x:int(x+.5) if x>=0 else -int(-x+.5)
rows=[]
for o in rd("branch_sales.csv"):
    r=dict(id=o["line_id"],br=o["branch"],code=o["product_code"],qty=float(o["qty"]),uom=o["uom"],price=float(o["unit_price"]))
    r["c"]=norm(r["code"]);r["q"]=r["qty"];r["pr"]=r["price"];r["fl"]=[];r["rev"]=False;p=M.get(r["c"])
    if not p: r["fl"].append("orphan");r["rev"]=True
    else:
        if r["code"]!=r["c"]: r["fl"].append("variant")
        if r["uom"]=="DZ": r["q"]*=12;r["fl"].append("dz")
        if r["uom"]=="L" and p["ml"]: r["q"]=rnd(r["q"]*1000/p["ml"]);r["fl"].append("unitL")
        if r["q"]<0: r["fl"].append("neg");r["rev"]=True
        k=r["pr"]/p["price"]
        if 9.5<k<10.5: r["pr"]=p["price"];r["fl"].append("price10")
    rows.append(r)
def metrics(k):
    rev=gp=um=0
    for r in rows:
        c=r["c"] if k>=1 else r["code"];q=r["qty"];pr=r["price"];p=M.get(c)
        if k>=2 and p:
            if r["uom"]=="DZ":q*=12
            if r["uom"]=="L" and p["ml"]:q=rnd(q*1000/p["ml"])
        if k>=3 and p and 9.5<pr/p["price"]<10.5: pr=p["price"]
        if k>=5 and (not p or q<0): continue
        s=q*pr;rev+=s
        if p: gp+=s-q*(p["sup"] if k>=4 else p["erp"])
        else: gp+=s;um+=s
    return gp/rev,um,rev
names=["Raw report","1 Match every code","2 Fix units","3 Correct prices","4 Use supplier costs","5 Set aside what can't be fixed"]
print("%-34s %8s %14s"%("Step","Margin","Unmapped KSh"))
for k in range(6):
    m,u,v=metrics(k);print("%-34s %7.1f%% %14s"%(names[k],m*100,format(round(u),",")))
planted=[r for r in rows if KEY[r["id"]]["defect"]];flag=[r for r in rows if r["fl"]]
hit=[r for r in planted if KEY[r["id"]]["defect"] in r["fl"]]
fixable=[r for r in planted if KEY[r["id"]]["defect"] in("variant","dz","unitL","price10")]
exact=[r for r in fixable if not r["rev"] and r["c"]==KEY[r["id"]]["true_code"] and r["q"]==float(KEY[r["id"]]["true_qty"]) and r["pr"]==float(KEY[r["id"]]["true_price"])]
print("caught %.1f%% | flags real %.1f%% | fixed exactly %.1f%% | review lines %d"%(100*len(hit)/len(planted),100*len([r for r in flag if KEY[r["id"]]["defect"]])/len(flag),100*len(exact)/len(fixable),sum(r["rev"] for r in rows)))
with open("output/cleaned_sales.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["line_id","branch","product_code","qty_items","unit_price"])
    for r in rows:
        if not r["rev"]: w.writerow([r["id"],r["br"],r["c"],r["q"],r["pr"]])
with open("output/review_queue.csv","w",newline="") as f:
    w=csv.writer(f);w.writerow(["line_id","branch","product_code","qty","unit_price","reason"])
    for r in rows:
        if r["rev"]: w.writerow([r["id"],r["br"],r["code"],r["qty"],r["price"],"unknown code" if "orphan" in r["fl"] else "negative quantity"])
