import adsk.core, adsk.fusion, math
BASE=r'C:\Users\vicen\Desktop\G7 Control proyecto 2\02_Carcasa\v6_scripts'
def run(_c):
    log=open(BASE+r'\log_fix2.txt','w')
    def L(*a): log.write(' '.join(str(x) for x in a)+'\n'); log.flush()
    des=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct); root=des.rootComponent
    T=adsk.fusion.TemporaryBRepManager.get(); P=adsk.core.Point3D.create; V=adsk.core.Vector3D.create; Bt=adsk.fusion.BooleanTypes
    U=lambda v:v/10
    def cyl(x,y,r,z0,z1): return T.createCylinderOrCone(P(U(x),U(y),U(z0)),U(r),P(U(x),U(y),U(z1)),U(r))
    c=[o for o in root.occurrences if o.name.startswith('Carcasa G7 v6')][0].component; F=c.features
    # 1) quitar lengueta/ranura
    for i in range(F.count-1,-1,-1):
        f=F.item(i)
        if f.name in ('Tapa: ranura 1.3 x 1.5','Base: lengueta 1.0 x 1.2'): f.deleteMe()
    for s in list(c.sketches):
        if s.name.startswith('Labio'): s.deleteMe()
    L('labio viejo eliminado')
    # 2) faldon interior de encaje (no toca la piel exterior)
    base=c.bRepBodies.itemByName('Base inferior'); tapa=c.bRepBodies.itemByName('Tapa superior')
    rim=max([f for f in base.faces if isinstance(f.geometry,adsk.core.Plane) and abs(f.boundingBox.maxPoint.z)<1e-4 and abs(f.boundingBox.minPoint.z)<1e-4],key=lambda f:f.area)
    L('rim area',round(rim.area*100),'loops',rim.loops.count)
    inner=[l for l in rim.loops if not l.isOuter][0]
    sk=c.sketches.add(c.xYConstructionPlane); sk.name='Faldon interior encaje'
    oc=adsk.core.ObjectCollection.create()
    for e in inner.edges:
        for ent in sk.project(e): oc.add(ent)
    dp=sk.modelToSketchSpace(P(0,0,0)); new=set()
    for d in (0.035,0.135):
        for e in sk.offset(oc,dp,d): new.add(e.entityToken)
    best=None
    for pr in sk.profiles:
        if pr.profileLoops.count!=2: continue
        if all(pc.sketchEntity.entityToken in new for pl in pr.profileLoops for pc in pl.profileCurves): best=pr
    sk.isVisible=False
    ei=F.extrudeFeatures.createInput(best,adsk.fusion.FeatureOperations.JoinFeatureOperation)
    ei.setDistanceExtent(False,adsk.core.ValueInput.createByReal(0.18)); ei.participantBodies=[base]
    F.extrudeFeatures.add(ei).name='Base: faldon interior de encaje 1.0 x 1.8'
    L('faldon ok')
    # 3) agujero stick mas grande para la cupula
    tapa=c.bRepBodies.itemByName('Tapa superior')
    bf=F.baseFeatures.add(); bf.startEdit(); c.bRepBodies.add(cyl(-2,-20,15.6,12.0,20),bf); bf.finishEdit(); bf.name='Tapa: agujero stick D31.2 (cupula)'
    o2=adsk.core.ObjectCollection.create(); o2.add(bf.bodies.item(0))
    ci=F.combineFeatures.createInput(tapa,o2); ci.operation=adsk.fusion.FeatureOperations.CutFeatureOperation; F.combineFeatures.add(ci).name='Tapa: agujero stick D31.2 (op)'
    L('agujero ok')
    # 4) perilla con cupula
    for o in list(root.occurrences):
        if o.name.startswith('Perilla joystick'): o.deleteMe()
    mg=[o for o in root.occurrences if o.name.startswith('Modelos')][0]
    ky=[o for o in mg.childOccurrences if o.name.startswith('KY')][0]
    j=[o for o in ky.childOccurrences if o.name.startswith('3D-Analog')][0]
    rot=[o for o in j.childOccurrences if o.name.startswith('Rotator')][0].bRepBodies.item(0)
    statics=[o.bRepBodies.item(0) for o in j.childOccurrences if not o.name.startswith('Rotator')]
    for o in ky.childOccurrences:
        if o.name.startswith('BaseBoard'):
            for ch in o.childOccurrences: statics.append(ch.bRepBodies.item(0))
    cx,cy,zp=-2.0,-20.0,14.61
    Ro,Ri,th=15.0,13.8,65.0
    dome=T.createSphere(P(U(cx),U(cy),U(zp)),U(Ro)); T.booleanOperation(dome,T.createSphere(P(U(cx),U(cy),U(zp)),U(Ri)),Bt.DifferenceBooleanType)
    hcut=Ro*math.cos(math.radians(th))
    T.booleanOperation(dome,cyl(cx,cy,Ro+1,zp+hcut,zp+Ro+1),Bt.IntersectionBooleanType)
    kn=cyl(cx,cy,10.5,27.6,29.6)
    T.booleanOperation(kn,dome,Bt.UnionBooleanType)
    T.booleanOperation(kn,cyl(cx,cy,3.6,21.8,27.9),Bt.UnionBooleanType)
    T.booleanOperation(kn,T.createSphere(P(U(cx),U(cy),U(29.6+30-1.0)),U(30)),Bt.DifferenceBooleanType)
    T.booleanOperation(kn,T.copy(rot),Bt.DifferenceBooleanType)
    T.booleanOperation(kn,cyl(cx,cy,2.2,26.31,26.5),Bt.DifferenceBooleanType)
    occ2=root.occurrences.addNewComponent(adsk.core.Matrix3D.create()); c2=occ2.component; c2.name='Perilla joystick con cupula (impresa)'
    bf=c2.features.baseFeatures.add(); bf.startEdit(); c2.bRepBodies.add(kn,bf); bf.finishEdit(); bf.name='Perilla D21 + cupula R15 centrada en el pivote (z14.61)'
    kb=c2.bRepBodies.item(0); kb.name='Perilla joystick con cupula'
    ap={a.name:a for a in des.appearances}
    if 'G7 capuchon negro' in ap: kb.appearance=ap['G7 capuchon negro']
    L('perilla ok tope sobre tapa', 29.6-14.8)
    # chequeos inclinacion
    tcopy=T.copy(c.bRepBodies.itemByName('Tapa superior'))
    worst={}
    for ax in (V(1,0,0),V(0,1,0),V(1,1,0),V(1,-1,0)):
        ax.normalize()
        for ang in (0,25,-25):
            t=T.copy(kb); m=adsk.core.Matrix3D.create(); m.setToRotation(math.radians(ang),ax,P(U(cx),U(cy),U(zp))); T.transform(t,m)
            for nm,ob in [('tapa',tcopy)]+[('KY:'+s.parentComponent.name if False else 'KY fijo %d'%i,s) for i,s in enumerate(statics)]:
                x=T.copy(t); T.booleanOperation(x,T.copy(ob),Bt.IntersectionBooleanType)
                v=round(x.volume*1000,3)
                if v>0: L('CHOQUE',nm,'eje',(round(ax.x,2),round(ax.y,2)),'ang',ang,v)
                worst[nm]=max(worst.get(nm,0),v)
    L('max choques',worst)
    # 5) colores capuchones
    cc=[o for o in root.occurrences if o.name.startswith('Capuchones impresos')][0].component
    cmap={'UP':'G7 capuchon rojo','DOWN':'G7 capuchon amarillo','LEFT':'G7 capuchon azul','RIGHT':'G7 capuchon verde','A':'G7 capuchon negro','B':'G7 capuchon negro'}
    for b in cc.bRepBodies:
        k=b.name.split()[1]
        if cmap.get(k) in ap: b.appearance=ap[cmap[k]]
    L('colores ok')
    # fuera del REF
    for nm in ('Tapa superior','Base inferior'):
        t=T.copy(c.bRepBodies.itemByName(nm)); T.booleanOperation(t,T.copy(c.bRepBodies.itemByName('REF exterior v6')),Bt.DifferenceBooleanType)
        L(nm,'fuera del REF mm3',round(t.volume*1000,3))
    L('FIN'); log.close()
