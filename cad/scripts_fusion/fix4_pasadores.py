# Control G7 v6.1 - pasadores de alineacion en la union de los grips (2 por grip)
# Torre D7 a cada lado de la union; pasador D3 x 4 mm en la tapa, agujero D3.3 x 4.8 en la base.
import adsk.core, adsk.fusion, traceback
BASE=r'C:\Users\vicen\Desktop\G7 Control proyecto 2'
SCR=BASE+r'\02_Carcasa\v6_scripts'
def run(_c):
    log=open(SCR+r'\log_fix4.txt','w',encoding='utf-8')
    def L(*a): log.write(' '.join(str(x) for x in a)+'\n'); log.flush()
    try:
        app=adsk.core.Application.get(); des=adsk.fusion.Design.cast(app.activeProduct)
        c=[o for o in des.rootComponent.occurrences if o.component.name=='Carcasa G7 v6'][0].component
        F=c.features; P=adsk.core.Point3D.create; V=adsk.core.ValueInput.createByReal
        T=adsk.fusion.TemporaryBRepManager.get(); BT=adsk.fusion.BooleanTypes
        if F.combineFeatures.itemByName('Tapa: pasadores de alineacion grips'):
            L('YA APLICADO'); log.close(); return
        tapa=c.bRepBodies.itemByName('Tapa superior'); base=c.bRepBodies.itemByName('Base inferior')
        ref=c.bRepBodies.itemByName('REF exterior v6')
        L('antes tapa %.2f base %.2f'%(tapa.volume,base.volume))
        zc=[(0,-0.03),(-2,-0.1),(-3.6,-0.45),(-5,-1.1),(-6.4,-1.75),(-7.7,-2.35),(-8.155,-2.44),
            (-8.48,-2.506),(-8.74,-2.558),(-8.909,-2.59),(-9.0,-2.61),(-10.2,-2.70)]
        def interp(tab,y):
            for (y1,z1),(y2,z2) in zip(tab,tab[1:]):
                if y2<=y<=y1: return z1+(z2-z1)*(y1-y)/(y1-y2)
            return tab[-1][1]
        Y0,Y1=-1.5,-2.5
        def zp(y):
            if y>=Y0: return 0.0
            s=min(1.0,(Y0-y)/(Y0-Y1)); s=s*s*(3-2*s); return interp(zc,y)*s
        # bordes interior/exterior del grip a la altura de la union (de las secciones del loft)
        xin=[(-5,5.4),(-6.4,5.85),(-7.7,6.3),(-8.155,6.46)]
        xout=[(-5,9.1),(-6.4,9.15),(-7.7,9.2),(-8.155,9.18)]
        spots=[(-6.0,'out'),(-8.0,'in')]
        R_BOSS,R_PIN,R_HOLE,IN=0.35,0.15,0.165,0.40
        up_list=[]; dn_list=[]; hole_list=[]
        refb=T.copy(ref)
        for side in (1,-1):
            # region de la union de ese grip (igual que fix3), como cuerpo temporal
            for y,wall in spots:
                z=zp(y)
                xw=interp(xout,y)-IN if wall=='out' else interp(xin,y)+IN
                x=side*xw
                boss=T.createCylinderOrCone(P(x,y,z-0.5),R_BOSS,P(x,y,z+0.5),R_BOSS)
                T.booleanOperation(boss,T.copy(refb),BT.IntersectionBooleanType)
                # mitad sobre la union (z > zp local): cortar con una caja inclinada -> se aproxima con
                # la superficie real: puntos sobre la union van a la tapa
                # construimos el semiespacio con un prisma a partir de la linea de union en y
                hi=T.copy(boss); lo=T.copy(boss)
                # prisma: secciones y-0.6..y+0.6 bajo la union
                ys=[y+0.6-0.1*i for i in range(13)]
                pts=[P(x-0.6,yy,zp(yy)) for yy in ys]
                # caja bajo la union aproximada por cajas finas de 1 mm en y
                below=None
                for yy in ys:
                    zz=zp(yy)
                    bx=adsk.core.OrientedBoundingBox3D.create(P(x,yy,zz-1.0),adsk.core.Vector3D.create(1,0,0),
                        adsk.core.Vector3D.create(0,1,0),1.4,0.1001,2.0)
                    b=T.createBox(bx)
                    if below is None: below=b
                    else: T.booleanOperation(below,b,BT.UnionBooleanType)
                T.booleanOperation(hi,T.copy(below),BT.DifferenceBooleanType)
                T.booleanOperation(lo,T.copy(below),BT.IntersectionBooleanType)
                pin=T.createCylinderOrCone(P(x,y,z-0.40),R_PIN,P(x,y,z+0.30),R_PIN)
                T.booleanOperation(hi,pin,BT.UnionBooleanType)
                hole=T.createCylinderOrCone(P(x,y,z-0.48),R_HOLE,P(x,y,z+0.05),R_HOLE)
                up_list.append(hi); dn_list.append(lo); hole_list.append(hole)
                L('pasador',side,y,wall,'x=%.2f z=%.2f  torre arriba %.3f abajo %.3f'%(x*10,z*10,hi.volume,lo.volume))
        def add(bodies,name):
            bf=F.baseFeatures.add(); bf.startEdit()
            for b in bodies: c.bRepBodies.add(b,bf)
            bf.finishEdit(); bf.name=name; return [bf.bodies.item(i) for i in range(bf.bodies.count)]
        def comb(target,tools,name,op):
            oc=adsk.core.ObjectCollection.create()
            for t in tools: oc.add(t)
            ci=F.combineFeatures.createInput(target,oc); ci.operation=op
            F.combineFeatures.add(ci).name=name
        J=adsk.fusion.FeatureOperations.JoinFeatureOperation; C=adsk.fusion.FeatureOperations.CutFeatureOperation
        comb(tapa,add(up_list,'Torres + pasadores (tapa)'),'Tapa: pasadores de alineacion grips',J)
        base=c.bRepBodies.itemByName('Base inferior')
        comb(base,add(dn_list,'Torres pasadores (base)'),'Base: torres pasadores grips',J)
        base=c.bRepBodies.itemByName('Base inferior')
        comb(base,add(hole_list,'Agujeros pasadores (base)'),'Base: agujeros D3.3 pasadores',C)
        tapa=c.bRepBodies.itemByName('Tapa superior'); base=c.bRepBodies.itemByName('Base inferior')
        for b in (tapa,base): L('%s %.2f cm3, %d lumps'%(b.name,b.volume,b.lumps.count))
        # que nada salga del exterior
        for b in (tapa,base):
            o=T.copy(b); T.booleanOperation(o,T.copy(refb),BT.DifferenceBooleanType)
            L('fuera del exterior',b.name,'%.4f cm3'%(o.volume if o.lumps.count else 0))
        em=des.exportManager; out=BASE+r'\06_Entrega_feedback_profe\STL_para_imprimir'
        for b,fn in ((tapa,'01_Tapa_superior.stl'),(base,'02_Base_inferior.stl')):
            o=em.createSTLExportOptions(b,out+'\\'+fn); o.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            em.execute(o); L('STL',fn)
        L('FIN OK')
    except:
        L('ERROR'); L(traceback.format_exc()); log.close(); raise
    log.close()
