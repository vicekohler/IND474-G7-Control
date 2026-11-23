import adsk.core, adsk.fusion, math
BASE=r'C:\Users\vicen\Desktop\G7 Control proyecto 2\02_Carcasa\v6_scripts'
def run(_c):
    log=open(BASE+r'\log_extras.txt','w')
    def L(*a): log.write(' '.join(str(x) for x in a)+'\n'); log.flush()
    des=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct); root=des.rootComponent
    T=adsk.fusion.TemporaryBRepManager.get(); P=adsk.core.Point3D.create; V=adsk.core.Vector3D.create; Bt=adsk.fusion.BooleanTypes
    U=lambda v:v/10
    def cyl(x,y,r,z0,z1): return T.createCylinderOrCone(P(U(x),U(y),U(z0)),U(r),P(U(x),U(y),U(z1)),U(r))
    def box(cx,cy,w,h,z0,z1): return T.createBox(adsk.core.OrientedBoundingBox3D.create(P(U(cx),U(cy),U((z0+z1)/2)),V(1,0,0),V(0,1,0),U(w),U(h),U(z1-z0)))
    # ---- capuchones mas altos (tope z17.3)
    for o in list(root.occurrences):
        if o.name.startswith(('Capuchones impresos','Perilla joystick')): o.deleteMe()
    est=[o for o in root.occurrences if o.name.startswith('Capuchones reales')][0]
    apsrc={b.name.split()[1]:b.appearance for b in est.bRepBodies}; est.isLightBulbOn=False
    occ=root.occurrences.addNewComponent(adsk.core.Matrix3D.create()); c=occ.component; c.name='Capuchones impresos (huecos con nervios)'
    BT=[('A',51.5,-1),('B',35.5,-9),('UP',-40.5,11),('DOWN',-40.5,-18),('LEFT',-53,-3.5),('RIGHT',-28,-3.5)]
    TOP=17.3; RF=TOP-1.2
    bf=c.features.baseFeatures.add(); bf.startEdit()
    for n,x,y in BT:
        cap=cyl(x,y,6.5,5.4,TOP); T.booleanOperation(cap,cyl(x,y,5.3,5.0,RF),Bt.DifferenceBooleanType)
        inner=cyl(x,y,3.6,5.0,RF)
        for (w,h) in ((10.8,1.0),(1.0,10.8)): T.booleanOperation(inner,box(x,y,w,h,5.4,RF),Bt.UnionBooleanType)
        T.booleanOperation(inner,cyl(x,y,5.3,5.0,RF),Bt.IntersectionBooleanType)
        T.booleanOperation(cap,inner,Bt.UnionBooleanType)
        T.booleanOperation(cap,box(x,y,3.95,3.95,4.0,7.5),Bt.DifferenceBooleanType)
        c.bRepBodies.add(cap,bf)
    bf.finishEdit(); bf.name='Capuchones D13 huecos, sobresalen 2.5 mm (tope z17.3)'
    for i,b in enumerate(bf.bodies): b.name='Capuchon %s D13 hueco (tope z17.3)'%BT[i][0]
    sel=adsk.core.ObjectCollection.create()
    for b in c.bRepBodies:
        for e in b.edges:
            bb=e.boundingBox
            if abs(bb.maxPoint.z-U(TOP))<1e-4 and abs(bb.minPoint.z-U(TOP))<1e-4 and isinstance(e.geometry,adsk.core.Circle3D) and abs(e.geometry.radius-0.65)<1e-4: sel.add(e)
    fi=c.features.filletFeatures.createInput(); fi.addConstantRadiusEdgeSet(sel,adsk.core.ValueInput.createByReal(0.08),True)
    c.features.filletFeatures.add(fi).name='Redondeo techo R0.8'
    for b in c.bRepBodies:
        k=b.name.split()[1]
        if apsrc.get(k): b.appearance=apsrc[k]
    L('capuchones ok')
    # ---- perilla baja
    mg=[o for o in root.occurrences if o.name.startswith('Modelos')][0]
    ky=[o for o in mg.childOccurrences if o.name.startswith('KY')][0]
    thumb=[o for o in ky.childOccurrences if o.name.startswith('Thumb')][0]
    j=[o for o in ky.childOccurrences if o.name.startswith('3D-Analog')][0]
    rot=[o for o in j.childOccurrences if o.name.startswith('Rotator')][0].bRepBodies.item(0)
    thumb.isLightBulbOn=False
    cx,cy=-2.0,-20.0
    kn=cyl(cx,cy,10.5,24.6,28.6)
    T.booleanOperation(kn,cyl(cx,cy,3.6,21.8,24.6),Bt.UnionBooleanType)
    sph=T.createSphere(P(U(cx),U(cy),U(28.6+30-1.0)),U(30)); T.booleanOperation(kn,sph,Bt.DifferenceBooleanType)
    rc=T.copy(rot); T.booleanOperation(kn,rc,Bt.DifferenceBooleanType)
    T.booleanOperation(kn,cyl(cx,cy,2.2,26.31,26.5),Bt.DifferenceBooleanType)
    occ2=root.occurrences.addNewComponent(adsk.core.Matrix3D.create()); c2=occ2.component; c2.name='Perilla joystick baja (impresa)'
    bf=c2.features.baseFeatures.add(); bf.startEdit(); c2.bRepBodies.add(kn,bf); bf.finishEdit(); bf.name='Perilla D21 baja (tope z28.6, encaje D al vastago)'
    kb=c2.bRepBodies.item(0); kb.name='Perilla joystick baja D21'
    try:
        es=adsk.core.ObjectCollection.create()
        for e in kb.edges:
            if isinstance(e.geometry,adsk.core.Circle3D) and abs(e.geometry.radius-1.05)<1e-4: es.add(e)
        fi=c2.features.filletFeatures.createInput(); fi.addConstantRadiusEdgeSet(es,adsk.core.ValueInput.createByReal(0.1),True)
        c2.features.filletFeatures.add(fi).name='Redondeo borde R1'
    except Exception as ex: L('fillet perilla',str(ex)[:80])
    ap={a.name:a for a in des.appearances}
    if 'G7 capuchon negro' in ap: kb.appearance=ap['G7 capuchon negro']
    L('perilla ok, tope sobre tapa mm', 28.6-14.8)
    # ---- chequeo inclinacion 25 grados contra la tapa
    cv=[o for o in root.occurrences if o.name.startswith('Carcasa G7 v6')][0].component
    tapa=T.copy(cv.bRepBodies.itemByName('Tapa superior'))
    orig=T.copy([o for o in mg.childOccurrences if o.name.startswith('KY')][0].childOccurrences.item(2).bRepBodies.item(0)) if False else None
    for nm,body in (('perilla baja',kb),):
        for zp in (13.0,15.0):
            for axis in (V(1,0,0),V(0,1,0)):
                for ang in (25,-25):
                    t=T.copy(body); m=adsk.core.Matrix3D.create(); m.setToRotation(math.radians(ang),axis,P(U(cx),U(cy),U(zp))); T.transform(t,m)
                    r=T.copy(rot); T.transform(r,m)
                    T.booleanOperation(t,r,Bt.UnionBooleanType)
                    T.booleanOperation(t,T.copy(tapa),Bt.IntersectionBooleanType)
                    L(nm,'pivote z',zp,'eje',(axis.x,axis.y),'ang',ang,'choque mm3',round(t.volume*1000,3))
    L('FIN EXTRAS'); log.close()
