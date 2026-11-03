"""Generates the practice data for the Naivas demo (fixed seed, so output is identical every run)."""
import csv, math, re
def rng(seed):
    st=[seed&0xFFFFFFFF]
    def r():
        st[0]=(st[0]+0x6D2B79F5)&0xFFFFFFFF; s=st[0]
        t=((s^(s>>15))*(1|s))&0xFFFFFFFF
        t=((t+(((t^(t>>7))*(61|t))&0xFFFFFFFF))&0xFFFFFFFF)^t
        return ((t^(t>>14))&0xFFFFFFFF)/4294967296
    return r
R=rng(20261030); rnd=lambda x:math.floor(x+.5)
CAT=[("Beverages",["Soda 500ml","Juice 1L","Water 1.5L","Soda 2L","Tea 100s"]),("Dairy",["Milk 500ml","Milk 1L","Yoghurt 500ml","Butter 250g","Cheese 200g"]),
("Bakery",["Bread 400g","Bread 800g","Buns 6s","Cake slice","Doughnut"]),("Cooking oils",["Cooking oil 1L","Cooking oil 3L","Margarine 500g","Ghee 500g","Cooking oil 5L"]),
("Household",["Detergent 1kg","Bleach 750ml","Dish soap 500ml","Tissue 10s","Mop head"]),("Personal care",["Soap bar","Lotion 400ml","Toothpaste 100ml","Shampoo 400ml","Deodorant"]),
("Snacks",["Crisps 100g","Biscuits 200g","Popcorn 150g","Nuts 250g","Chocolate 100g"]),("Grains",["Maize flour 2kg","Rice 2kg","Wheat flour 2kg","Sugar 2kg","Beans 1kg"])]
MG={"Beverages":.2,"Dairy":.14,"Bakery":.28,"Cooking oils":.1,"Household":.3,"Personal care":.35,"Snacks":.25,"Grains":.08}
P=[];n=1000;i=0
for c,names in CAT:
    for nm in names:
        price=rnd(60+R()*540); sup=rnd(price*(1-MG[c]*(.8+R()*.4)))
        erp=rnd(sup*(.72+R()*.16)) if i%5==2 else sup; i+=1
        base=20+R()*80; m=re.search(r'(\d+(?:\.\d+)?)(ml|L)\b',nm)
        ml=(float(m.group(1))*1000 if m.group(2)=="L" else float(m.group(1))) if m else 0
        P.append(dict(code="NV-%d"%n,name=nm,cat=c,price=price,sup=sup,erp=erp,base=base,ml=int(ml))); n+=1
M={p["code"]:p for p in P}
VAR=[lambda d:"nv-"+d,lambda d:d+"-NV",lambda d:"NV"+d,lambda d:"NV "+d]
sales=[];key=[];lid=0
for b in range(12):
    bs=.8+R()*.4
    for w in range(8):
        for p in P:
            q=max(1,rnd(p["base"]*bs*(.8+R()*.4)*(2.2 if R()<.06 else 1)))
            d=p["code"][3:]; r=R(); df="";code=p["code"];qty=q;uom="EA";price=p["price"];tq=q
            if r<.11:
                df="variant";code=VAR[math.floor(R()*4)](d)
                if R()<.15:
                    sw=d[:2]+d[3]+d[2]
                    if "NV-"+sw in M and sw!=d: code="NV-"+sw
            elif r<.135:
                df="dz";tq=max(1,rnd(q/12))*12;qty=tq//12;uom="DZ"
            elif r<.16:
                if p["ml"]: df="unitL";qty=q*p["ml"]/1000;uom="L"
            elif r<.175:
                if R()<.4: df="price10";price=p["price"]*10
            elif r<.19:
                df="orphan";code="NV-9%d"%math.floor(100+R()*899)
            elif r<.2:
                df="neg";qty=-q
            lid+=1
            sales.append([lid,b+1,w+1,code,qty,uom,price]); key.append([lid,p["code"],tq,p["price"],df])
def wr(f,h,rows):
    with open("data/"+f,"w",newline="") as fh: w=csv.writer(fh); w.writerow(h); w.writerows(rows)
wr("item_master.csv",["code","name","category","shelf_price","erp_cost","size_ml"],[[p["code"],p["name"],p["cat"],p["price"],p["erp"],p["ml"]] for p in P])
wr("supplier_costs.csv",["code","supplier_cost"],[[p["code"],p["sup"]] for p in P])
wr("branch_sales.csv",["line_id","branch","week","product_code","qty","uom","unit_price"],sales)
wr("answer_key.csv",["line_id","true_code","true_qty","true_price","defect"],key)
print(len(sales),"sales lines written")
