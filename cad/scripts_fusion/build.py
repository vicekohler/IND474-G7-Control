import adsk.core, adsk.fusion, json, math
BASE=r'C:\Users\vicen\Desktop\G7 Control proyecto 2\02_Carcasa\v6_scripts'
def run(_c):
    D=json.load(open(BASE+r'\v6_data.json'))
    log=open(BASE+r'\log_build.txt','w')
    def L(*a): log.write(' '.join(str(x) for x in a)+'\n'); log.flush()
    app=adsk.core.Application.get(); des=adsk.fusion.Design.cast(app.activeProduct)
    root=des.rootComponent
    for o in list(root.occurrences):
        if o.name.startswith('Carcasa G7 v6'): o.deleteMe()
    occ=root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    c=occ.component; c.name='Carcasa G7 v6'
    P=adsk.core.Point3D.create; F=c.features; NB=adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    def plane_off(base,v):
        pi=c.constructionPlanes.createInput(); pi.setByOffset(base,adsk.core.ValueInput.createByReal(v)); pl=c.constructionPlanes.add(pi); pl.isLightBulbOn=False; return pl
    def spline(sk,pts3):
        oc=adsk.core.ObjectCollection.create()
        for p in pts3: oc.add(sk.modelToSketchSpace(p))
        sp=sk.sketchCurves.sketchFittedSplines.add(oc); sp.isClosed=True; return sp
    t=plane_off(c.xZConstructionPlane,1.0); sgn=1 if t.geometry.origin.y>0 else -1; t.deleteMe()
    def body_loft(secs,name):
        li=F.loftFeatures.createInput(NB)
        for z,pts in secs:
            sk=c.sketches.add(plane_off(c.xYConstructionPlane,z/10)); sk.name=name+' z=%g'%z
            spline(sk,[P(x,y,z/10) for x,y in pts]); sk.isVisible=False
            li.loftSections.add(sk.profiles.item(0))
        li.isSolid=True; lf=F.loftFeatures.add(li); lf.name=name; b=lf.bodies.item(0); b.name=name; return b
    def grip_loft(gr,tip,side,name):
        gl=F.loftFeatures.createInput(NB)
        for y,pts in gr:
            sk=c.sketches.add(plane_off(c.xZConstructionPlane,sgn*y)); sk.name=name+' y=%g'%(y*10)
            spline(sk,[P(side*x,y,z) for x,z in pts]); sk.isVisible=False
            gl.loftSections.add(sk.profiles.item(0))
        ty,tx,tz=tip
        sk=c.sketches.add(plane_off(c.xZConstructionPlane,sgn*ty)); sk.name=name+' punta'
        sp=sk.sketchPoints.add(sk.modelToSketchSpace(P(side*tx,ty,tz))); sk.isVisible=False
        ls=gl.loftSections.add(sp); ls.setPointTangentEndCondition(adsk.core.ValueInput.createByReal(1.0))
        gl.isSolid=True; lf=F.loftFeatures.add(gl); lf.name=name; b=lf.bodies.item(0); b.name=name; return b
    def comb(target,tools,name,op=adsk.fusion.FeatureOperations.JoinFeatureOperation):
        oc=adsk.core.ObjectCollection.create()
        for t in tools: oc.add(t)
        ci=F.combineFeatures.createInput(target,oc); ci.operation=op
        cf=F.combineFeatures.add(ci); cf.name=name; return cf
    body=body_loft(D['secs'],'Cuerpo v6')
    gd=grip_loft(D['grips'],D['tip'],1,'Grip der'); gi=grip_loft(D['grips'],D['tip'],-1,'Grip izq')
    comb(body,[gd,gi],'Union grips'); body=c.bRepBodies.item(0); body.name='Carcasa v6'
    L('cuerpo+grips ok')
    sel=adsk.core.ObjectCollection.create()
    for e in body.edges:
        if e.faces.count!=2: continue
        ex=e.evaluator.getParameterExtents(); _,mid=e.evaluator.getPointAtParameter((ex[1]+ex[2])/2)
        n=[f.evaluator.getNormalAtPoint(mid)[1] for f in e.faces]
        if math.degrees(n[0].angleTo(n[1]))>8 and abs(mid.z*10-14.8)>0.3 and abs(mid.z*10+15)>0.3: sel.add(e)
    L('aristas union',sel.count)
    for R in (0.8,0.6,0.4,0.25):
        try:
            fi=F.filletFeatures.createInput(); fi.addConstantRadiusEdgeSet(sel,adsk.core.ValueInput.createByReal(R),True)
            F.filletFeatures.add(fi).name='Union grips R%g'%(R*10); L('fillet union',R); break
        except Exception as ex: L('fail union',R)
    body=c.bRepBodies.item(0)
    fc=[f for f in body.faces if isinstance(f.geometry,adsk.core.Plane) and abs(f.boundingBox.minPoint.z-1.48)<1e-3 and abs(f.boundingBox.maxPoint.z-1.48)<1e-3]
    ft=max(fc,key=lambda f:f.area); sel=adsk.core.ObjectCollection.create()
    for e in ft.edges: sel.add(e)
    fi=F.filletFeatures.createInput(); fi.addConstantRadiusEdgeSet(sel,adsk.core.ValueInput.createByReal(0.4),True)
    F.filletFeatures.add(fi).name='Borde superior R4'; L('fillet top ok')
    body=c.bRepBodies.item(0)
    tb=adsk.fusion.TemporaryBRepManager.get().copy(body)
    bf=F.baseFeatures.add(); bf.startEdit(); c.bRepBodies.add(tb,bf); bf.finishEdit(); bf.name='REF solido exterior v6'
    for b in c.bRepBodies:
        if b!=body: b.name='REF exterior v6'; b.isLightBulbOn=False
    ib=body_loft(D['isecs'],'Hueco interior')
    igd=grip_loft(D['igrips'],D['itip'],1,'Hueco grip der'); igi=grip_loft(D['igrips'],D['itip'],-1,'Hueco grip izq')
    comb(ib,[igd,igi],'Hueco union')
    comb(body,[ib],'Vaciado manual 2 mm',adsk.fusion.FeatureOperations.CutFeatureOperation)
    L('vaciado ok')
    si=F.splitBodyFeatures.createInput(body,c.xYConstructionPlane,True)
    F.splitBodyFeatures.add(si).name='Particion z=0'
    for b in c.bRepBodies:
        if not b.isLightBulbOn: continue
        bb=b.boundingBox
        b.name='Tapa superior' if bb.minPoint.z>-0.01 else 'Base inferior'
        L(b.name,[round(v*10,1) for v in (bb.minPoint.x,bb.minPoint.y,bb.minPoint.z,bb.maxPoint.x,bb.maxPoint.y,bb.maxPoint.z)])
    L('FIN BUILD')
    log.close()
