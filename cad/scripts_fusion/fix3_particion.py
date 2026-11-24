# Control G7 v6.1 - particion que sigue la geometria de los grips (feedback del profesor 24/11)
# En el cuerpo la particion sigue en z=0. En cada grip baja por la linea media de la seccion
# hasta la punta, asi cada mitad del grip es una cascara abierta que se imprime sin soporte interior.
import adsk.core, adsk.fusion, traceback, os
BASE=r'C:\Users\vicen\Desktop\G7 Control proyecto 2'
SCR=BASE+r'\02_Carcasa\v6_scripts'
def run(_c):
    log=open(SCR+r'\log_fix3.txt','w',encoding='utf-8')
    def L(*a): log.write(' '.join(str(x) for x in a)+'\n'); log.flush()
    try:
        app=adsk.core.Application.get(); des=adsk.fusion.Design.cast(app.activeProduct)
        root=des.rootComponent
        occ=[o for o in root.occurrences if o.component.name=='Carcasa G7 v6'][0]
        c=occ.component; F=c.features; P=adsk.core.Point3D.create; V=adsk.core.ValueInput.createByReal
        tapa=c.bRepBodies.itemByName('Tapa superior'); base=c.bRepBodies.itemByName('Base inferior')
        L('antes tapa %.2f cm3  base %.2f cm3'%(tapa.volume,base.volume))
        # el faldon de encaje habia quedado como cuerpo suelto (z 0..1.8 mm): se une a la base
        for b in list(c.bRepBodies):
            bb=b.boundingBox
            if b.name.startswith('Cuerpo') and abs(bb.minPoint.z)<1e-3 and abs(bb.maxPoint.z-0.18)<1e-3 and b.volume<2:
                oc=adsk.core.ObjectCollection.create(); oc.add(b)
                ci=F.combineFeatures.createInput(base,oc); ci.operation=adsk.fusion.FeatureOperations.JoinFeatureOperation
                F.combineFeatures.add(ci).name='Base: une faldon de encaje'
                base=c.bRepBodies.itemByName('Base inferior'); L('faldon unido a la base', round(base.volume,2))
        if c.features.combineFeatures.itemByName('Tapa: mitad superior de los grips'):
            L('YA APLICADO, no se hace nada'); log.close(); return
        # linea media de los grips (centro z de cada seccion del loft, cm)
        zc=[(0,-0.03),(-2,-0.1),(-3.6,-0.45),(-5,-1.1),(-6.4,-1.75),(-7.7,-2.35),(-8.155,-2.44),
            (-8.48,-2.506),(-8.74,-2.558),(-8.909,-2.59),(-9.0,-2.61),(-10.2,-2.70)]
        def interp(y):
            if y>=zc[0][0]: return zc[0][1]
            for (y1,z1),(y2,z2) in zip(zc,zc[1:]):
                if y2<=y<=y1: return z1+(z2-z1)*(y1-y)/(y1-y2)
            return zc[-1][1]
        Y0,Y1=-1.5,-2.5          # transicion suave desde el borde trasero del cuerpo
        def zp(y):
            if y>=Y0: return 0.0
            s=min(1.0,(Y0-y)/(Y0-Y1)); s=s*s*(3-2*s); return interp(y)*s
        X0,X1=4.6,10.5           # franja de los grips (a cada lado)
        ys=[Y0-0.2*i for i in range(45)]   # -5.0 ... -10.0
        def plane_x(x):
            pi=c.constructionPlanes.createInput(); pi.setByOffset(c.yZConstructionPlane,V(x))
            pl=c.constructionPlanes.add(pi); pl.isLightBulbOn=False; return pl
        def region(side,name,top_only=False):
            x=side*X0; sk=c.sketches.add(plane_x(x)); sk.name=name; sk.isVisible=False
            S=lambda y,z: sk.modelToSketchSpace(P(x,y,z))
            ln=sk.sketchCurves.sketchLines
            if top_only:   # franja z 0..0.25 para quitar el faldon dentro de los grips
                ln.addTwoPointRectangle(S(Y0,0.0),S(ys[-1],0.25))
            else:
                oc=adsk.core.ObjectCollection.create()
                for y in ys: oc.add(S(y,zp(y)))
                sp=sk.sketchCurves.sketchFittedSplines.add(oc)
                a=ln.addByTwoPoints(sp.endSketchPoint,S(ys[-1],0.0))
                ln.addByTwoPoints(a.endSketchPoint,sp.startSketchPoint)
            prof=sk.profiles.item(0)
            ei=F.extrudeFeatures.createInput(prof,adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            ei.setDistanceExtent(False,V(side*(X1-X0)))
            ef=F.extrudeFeatures.add(ei); ef.name=name; b=ef.bodies.item(0); b.name=name; b.isLightBulbOn=False
            return b
        Rd=region(1,'Zona grip der (z media..0)'); Ri=region(-1,'Zona grip izq (z media..0)')
        Fd=region(1,'Faldon grip der',True); Fi=region(-1,'Faldon grip izq',True)
        T=adsk.fusion.TemporaryBRepManager.get()
        pb=T.copy(base); rb=T.copy(Rd); T.booleanOperation(rb,T.copy(Ri),adsk.fusion.BooleanTypes.UnionBooleanType)
        T.booleanOperation(pb,rb,adsk.fusion.BooleanTypes.IntersectionBooleanType)
        L('pieza que pasa a la tapa %.2f cm3'%pb.volume)
        bf=F.baseFeatures.add(); bf.startEdit(); c.bRepBodies.add(pb,bf); bf.finishEdit()
        bf.name='Mitad superior de los grips'
        piece=bf.bodies.item(0); piece.name='Mitad superior grips'
        oc=adsk.core.ObjectCollection.create()
        for t in (Rd,Ri,Fd,Fi): oc.add(t)
        ci=F.combineFeatures.createInput(base,oc); ci.operation=adsk.fusion.FeatureOperations.CutFeatureOperation
        F.combineFeatures.add(ci).name='Base: particion sigue la linea media del grip'
        oc=adsk.core.ObjectCollection.create(); oc.add(piece)
        ci=F.combineFeatures.createInput(tapa,oc); ci.operation=adsk.fusion.FeatureOperations.JoinFeatureOperation
        F.combineFeatures.add(ci).name='Tapa: mitad superior de los grips'
        tapa=c.bRepBodies.itemByName('Tapa superior'); base=c.bRepBodies.itemByName('Base inferior')
        for b in (tapa,base):
            bb=b.boundingBox
            L('%s: %.2f cm3, %d lumps, z %.1f..%.1f mm'%(b.name,b.volume,b.lumps.count,bb.minPoint.z*10,bb.maxPoint.z*10))
        # interferencia tapa-base
        L('suma tapa+base %.2f cm3'%(tapa.volume+base.volume))
        # exportar STL nuevos
        em=des.exportManager; out=BASE+r'\06_Entrega_feedback_profe\STL_para_imprimir'
        for b,fn in ((tapa,'01_Tapa_superior.stl'),(base,'02_Base_inferior.stl')):
            o=em.createSTLExportOptions(b,out+'\\'+fn); o.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
            em.execute(o); L('STL',fn)
        # renders
        vp=app.activeViewport; rd=BASE+r'\02_Carcasa\renders_v6'
        def shot(fn,eye,up):
            cam=vp.camera; cam.target=P(0,-2,0); cam.eye=P(*eye); cam.upVector=adsk.core.Vector3D.create(*up)
            cam.isSmoothTransition=False; vp.camera=cam; vp.fit(); vp.saveAsImageFile(rd+'\\'+fn,1800,1100); L('render',fn)
        shot('carcasa_v6_12_particion_lateral.png',(60,-2,0),(0,0,1))
        shot('carcasa_v6_13_particion_abajo.png',(0,-2,-60),(0,1,0))
        shot('carcasa_v6_14_particion_iso.png',(40,-45,-25),(0,0,1))
        L('FIN OK - revisar y guardar el documento')
    except:
        L('ERROR'); L(traceback.format_exc()); log.close(); raise
    log.close()
