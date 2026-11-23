import adsk.core, adsk.fusion, os, json, math
BASE=r'C:\Users\vicen\Desktop\G7 Control proyecto 2\02_Carcasa\v6_scripts'
def run(_c):
    D=json.load(open(BASE+r'\v6_data.json'))
    log=open(BASE+r'\log_finish.txt','w')
    def L(*a): log.write(' '.join(str(x) for x in a)+'\n'); log.flush()
    des=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root=des.rootComponent
    c5=[o for o in root.occurrences if o.name.startswith('Carcasa G7 v5')][0].component
    c=[o for o in root.occurrences if o.name.startswith('Carcasa G7 v6')][0].component
    F=c.features; T=adsk.fusion.TemporaryBRepManager.get(); P=adsk.core.Point3D.create; V=adsk.core.Vector3D.create
    B={b.name:b for b in c.bRepBodies}
    ref=T.copy(B['REF exterior v6'])
    U=lambda v:v/10
    def cyl(x,y,r,z0,z1): return T.createCylinderOrCone(P(U(x),U(y),U(z0)),U(r),P(U(x),U(y),U(z1)),U(r))
    def box(x0,x1,y0,y1,z0,z1):
        ob=adsk.core.OrientedBoundingBox3D.create(P((x0+x1)/20,(y0+y1)/20,(z0+z1)/20),V(1,0,0),V(0,1,0),(x1-x0)/10,(y1-y0)/10,(z1-z0)/10)
        return T.createBox(ob)
    def obox(cx,cy,cz,ld,wd,l,w,h):
        return T.createBox(adsk.core.OrientedBoundingBox3D.create(P(U(cx),U(cy),U(cz)),ld,wd,U(l),U(w),U(h)))
    def apply(target,tools,name,cut,clip=False):
        bf=F.baseFeatures.add(); bf.startEdit()
        for t in tools:
            if clip: T.booleanOperation(t,ref,adsk.fusion.BooleanTypes.IntersectionBooleanType)
            c.bRepBodies.add(t,bf)
        bf.finishEdit(); bf.name=name
        oc=adsk.core.ObjectCollection.create()
        for b in bf.bodies: oc.add(b)
        ci=F.combineFeatures.createInput(target,oc); ci.operation=adsk.fusion.FeatureOperations.CutFeatureOperation if cut else adsk.fusion.FeatureOperations.JoinFeatureOperation
        F.combineFeatures.add(ci).name=name+' (op)'; L(name)
    H=[(58.5,31),(-58.5,31),(58.5,-31),(-58.5,-31)]
    KY=[(10.5,-8.75),(-16,-8.75),(10.5,-29.25),(-16,-29.25)]
    M2=[(3.22,5.61),(37.44,5.61),(3.22,28.39),(37.44,28.39)]
    BT=[(51.5,-1),(35.5,-9),(-40.5,11),(-40.5,-18),(-53,-3.5),(-28,-3.5)]
    tapa=B['Tapa superior']; base=B['Base inferior']
    apply(tapa,[cyl(x,y,3.5,0,13.3) for x,y in H],'Tapa: postes PCB H1-H4 D7',False,True)
    apply(tapa,[cyl(x,y,3.0,7.63,13.3) for x,y in KY],'Tapa: torres KY-023 D6',False,True)
    apply(tapa,[cyl(x,y,7,9,20) for x,y in BT]+[cyl(49.5,23,3,9,20),cyl(-2,-20,14,9.8,20)],'Tapa: agujeros botones D14, MENU D6, stick D28',True)
    apply(tapa,[box(5.9,35.7,4.15,30.85,11.3,13.8),box(3.7,6.0,6.4,28.9,11.3,13.8)],'Tapa: rebaje vidrio pantalla (labio 1.0) + cinta flex',True)
    apply(tapa,[box(22.75-12.2,22.75+12.2,17.5-12.2,17.5+12.2,13.5,20)],'Tapa: ventana area visible 24.4x24.4',True)
    apply(tapa,[cyl(x,y,0.8,0,10.8) for x,y in H]+[cyl(x,y,1.1,7.63,11.8) for x,y in KY]+[cyl(x,y,2.5,12.0,13.6) for x,y in M2],'Tapa: pilotos M2 PCB (M2x6 desde abajo), M2.5 KY y cajeras cabezas M2',True)
    apply(base,[cyl(x,y,3.5,-60,-1.52) for x,y in H],'Base: apoyos PCB H1-H4 D7',False,True)
    apply(base,[cyl(x,y,2.3,-4.2,-1.52) for x,y in H],'Base: cajera cabeza M2 en apoyos (fondo sin tornillos)',True)
    apply(base,[box(-16.25,-2.75,30,60,-9.45,-1.95)],'Base: tunel USB-C 13.5x7.5',True)
    # clips a presion
    arms=[]; catches=[]
    for x0,y0,nx,ny in D['clips']:
        n=V(nx,ny,0); t=V(-ny,nx,0); z=V(0,0,1)
        def at(s): return (x0-nx*s, y0-ny*s)
        ax,ay=at(4.8); arms.append(obox(ax,ay,-1.5,n,t,1.2,7,15))
        hx,hy=at(3.8); arms.append(obox(hx,hy,4.8,n,t,0.8,7,0.8))
        dx,dy=at(4.2); a=V((nx)/math.sqrt(2),(ny)/math.sqrt(2),1/math.sqrt(2))
        arms.append(obox(dx,dy,5.2,a,t,1.131,7,1.131))
        kx,ky=at(2.75); catches.append(obox(kx,ky,3.65,n,t,2.5,7.4,1.3))
    apply(base,arms,'Base: 6 clips a presion (brazo 1.2 x 7, gancho 0.8)',False,True)
    apply(tapa,catches,'Tapa: 6 topes de enganche para clips',False,True)
    # nervio central en cada grip (soporte para imprimir y rigidez)
    ribs=[]
    for s in (1,-1):
        p0=(s*67.5,-24.0); p1=(s*79.3,-90.0); dx=p1[0]-p0[0]; dy=p1[1]-p0[1]; Ln=math.hypot(dx,dy)
        ld=V(dx/Ln,dy/Ln,0); wd=V(-dy/Ln,dx/Ln,0)
        ribs.append(obox((p0[0]+p1[0])/2,(p0[1]+p1[1])/2,-22,ld,wd,Ln,1.2,40))
    apply(base,ribs,'Base: nervio central grips 1.2 mm',False,True)
    # labio de encaje
    def ring(o_out,o_in,name):
        sk=c.sketches.add(c.xYConstructionPlane); sk.name=name
        rim=[f for f in c.bRepBodies.itemByName('Base inferior').faces if isinstance(f.geometry,adsk.core.Plane) and abs(f.boundingBox.maxPoint.z)<1e-4 and abs(f.boundingBox.minPoint.z)<1e-4]
        rim=max(rim,key=lambda f:f.area)
        new=set()
        dp=sk.modelToSketchSpace(P(0,4.56,0))
        for lp in rim.loops:
            oc=adsk.core.ObjectCollection.create()
            for e in lp.edges:
                for ent in sk.project(e): oc.add(ent)
            off=sk.offset(oc,dp,o_out if lp.isOuter else o_in)
            for e in off: new.add(e.entityToken)
        for e in sk.sketchCurves:
            pass
        best=None
        for pr in sk.profiles:
            if pr.profileLoops.count!=2: continue
            ok=all(pc.sketchEntity.entityToken in new for pl in pr.profileLoops for pc in pl.profileCurves)
            if ok: best=pr
        sk.isVisible=False
        return best
    try:
        pr=ring(0.09,0.05,'Labio (lengueta base)')
        ei=F.extrudeFeatures.createInput(pr,adsk.fusion.FeatureOperations.JoinFeatureOperation)
        ei.setDistanceExtent(False,adsk.core.ValueInput.createByReal(0.12)); ei.participantBodies=[c.bRepBodies.itemByName('Base inferior')]
        F.extrudeFeatures.add(ei).name='Base: lengueta 1.0 x 1.2'
        pr=ring(0.075,0.035,'Labio (ranura tapa)')
        ei=F.extrudeFeatures.createInput(pr,adsk.fusion.FeatureOperations.CutFeatureOperation)
        ei.setDistanceExtent(False,adsk.core.ValueInput.createByReal(0.15)); ei.participantBodies=[c.bRepBodies.itemByName('Tapa superior')]
        F.extrudeFeatures.add(ei).name='Tapa: ranura 1.3 x 1.5'
        L('labio ok')
    except Exception as ex: L('labio FALLO',str(ex)[:200])
    # bisel USB
    try:
        t=c.constructionPlanes.createInput(); t.setByOffset(c.xZConstructionPlane,adsk.core.ValueInput.createByReal(1)); tp=c.constructionPlanes.add(t); sg=1 if tp.geometry.origin.y>0 else -1; tp.deleteMe()
        li=F.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        for yv,w,h in ((42.0,13.5,7.5),(48.5,17.5,10.5)):
            pi=c.constructionPlanes.createInput(); pi.setByOffset(c.xZConstructionPlane,adsk.core.ValueInput.createByReal(sg*yv/10)); pl=c.constructionPlanes.add(pi); pl.isLightBulbOn=False
            sk=c.sketches.add(pl); sk.name='bisel USB y=%g'%yv
            zc=-5.7 if yv<45 else -6.0
            pts=[sk.modelToSketchSpace(P(U(-9.5+sx*w/2),U(yv),U(zc+sz*h/2))) for sx,sz in ((-1,-1),(1,-1),(1,1),(-1,1))]
            for i in range(4): sk.sketchCurves.sketchLines.addByTwoPoints(pts[i],pts[(i+1)%4])
            sk.isVisible=False; li.loftSections.add(sk.profiles.item(0))
        lf=F.loftFeatures.add(li); tb=lf.bodies.item(0)
        oc=adsk.core.ObjectCollection.create(); oc.add(tb)
        ci=F.combineFeatures.createInput(c.bRepBodies.itemByName('Base inferior'),oc); ci.operation=adsk.fusion.FeatureOperations.CutFeatureOperation
        F.combineFeatures.add(ci).name='Base: bisel entrada USB-C'; L('bisel ok')
    except Exception as ex: L('bisel FALLO',str(ex)[:200])
    tapa=c.bRepBodies.itemByName('Tapa superior'); base=c.bRepBodies.itemByName('Base inferior')
    s5=c5.sketches.itemByName('Graficos grabados')
    pi=c.constructionPlanes.createInput(); pi.setByOffset(c.xYConstructionPlane,adsk.core.ValueInput.createByReal(1.48)); pl=c.constructionPlanes.add(pi); pl.isLightBulbOn=False
    sk=c.sketches.add(pl); sk.name='Graficos grabados v6'
    oc=adsk.core.ObjectCollection.create()
    for l in s5.sketchCurves.sketchLines: oc.add(l)
    s5.copy(oc,adsk.core.Matrix3D.create(),sk)
    for t in s5.sketchTexts:
        bb=t.boundingBox
        ti=sk.sketchTexts.createInput2(t.text,t.height)
        ti.setAsMultiLine(P(bb.minPoint.x,bb.minPoint.y,0),P(bb.maxPoint.x,bb.maxPoint.y,0),adsk.core.HorizontalAlignments.CenterHorizontalAlignment,adsk.core.VerticalAlignments.MiddleVerticalAlignment,0)
        ti.fontName=t.fontName; ti.textStyle=t.textStyle
        sk.sketchTexts.add(ti)
    prof=adsk.core.ObjectCollection.create()
    for p in sk.profiles: prof.add(p)
    for t in sk.sketchTexts: prof.add(t)
    ei=F.extrudeFeatures.createInput(prof,adsk.fusion.FeatureOperations.CutFeatureOperation)
    ei.setDistanceExtent(False,adsk.core.ValueInput.createByReal(-0.04)); ei.participantBodies=[tapa]
    F.extrudeFeatures.add(ei).name='Grabado 0.4 mm'; sk.isVisible=False; L('grabado ok')
    ap={a.name:a for a in des.appearances}
    for b,n in ((tapa,'G7 tapa gris oscuro'),(base,'G7 base gris claro')):
        if n in ap:
            b.appearance=ap[n]
            for f in b.faces: f.appearance=ap[n]
    L('FIN FINISH'); log.close()
