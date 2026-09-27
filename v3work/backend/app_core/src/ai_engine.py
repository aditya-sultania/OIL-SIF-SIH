HIGH_RISK=['energized','live electrical','without isolation','not isolated','lockout','loto','stored energy','confined space','entered the vessel','vessel entry','without gas testing','without gas test','suspended load','falling object','line of fire','hot work','welding','flammable','work at height','without fall protection']
RULES={'Energy Isolation':['isolation','energized','live electrical','lockout','loto','tagout','stored energy'],'Confined Space':['confined space','vessel entry','entered the vessel','tank entry','gas testing','atmospheric testing'],'Hot Work':['hot work','welding','cutting','grinding','spark','flammable'],'Line of Fire':['line of fire','suspended load','falling object','caught between','pinch point','struck by'],'Work at Height':['work at height','height','scaffold','ladder','fall protection','harness'],'Safe Mechanical Lifting':['lifting','crane','rigging','suspended load'],'Work Authorisation':['permit to work','ptw','work permit']}
ACTIVITIES={'Maintenance':['maintenance','repair','servicing','overhaul'],'Confined-space entry':['confined space','vessel entry','tank entry','entered the vessel'],'Hot work':['hot work','welding','cutting','grinding'],'Lifting operation':['lifting','crane','rigging','suspended load'],'Electrical work':['electrical','energized','power supply','isolation'],'Work at height':['height','scaffold','ladder','harness'],'Inspection':['inspection','inspect','checking']}
def contains(t,words): return any(w in t.lower() for w in words)
def analyze_report(text):
 t=text.lower(); risks=[x for x in HIGH_RISK if x in t]; score=min(100,20+len(risks)*12); cls='HIGH' if score>=70 else 'MEDIUM' if score>=45 else 'LOW'
 rules=[r for r,w in RULES.items() if contains(text,w)] or ['Other / HSE Review']
 activity=next((a for a,w in ACTIVITIES.items() if contains(text,w)),'General operation')
 if contains(text,['electrical','energized','isolation','loto']): hazard='Uncontrolled electrical/stored energy'
 elif contains(text,['confined','vessel','gas testing','oxygen']): hazard='Hazardous atmosphere / confined-space exposure'
 elif contains(text,['lifting','crane','suspended load','falling object']): hazard='Struck-by / crushing / dropped-object exposure'
 elif contains(text,['hot work','welding','flammable','spark']): hazard='Fire / explosion / ignition'
 elif contains(text,['height','scaffold','ladder','fall']): hazard='Fall from height'
 else: hazard='Hazard not confidently identified'
 if contains(text,['isolation','loto','lockout','tagout']): barrier='Energy Isolation / LOTO'
 elif contains(text,['gas testing','gas test','atmospheric testing']): barrier='Gas testing'
 elif contains(text,['permit to work','ptw','work permit']): barrier='Permit to Work'
 elif contains(text,['harness','fall protection','guardrail']): barrier='Fall protection'
 elif contains(text,['barricade','exclusion zone']): barrier='Exclusion zone'
 else: barrier='Not identified'
 failure='Possible missing, failed or unverified safety barrier' if any(x in t for x in ['without','no ','not ','failed','missing','absent']) else 'Requires HSE review'
 if contains(text,['electrical','energized','electrocution']): consequence='Potential fatal electrocution / severe electrical injury'
 elif contains(text,['confined','vessel','gas','oxygen']): consequence='Potential fatal toxic exposure / asphyxiation'
 elif contains(text,['lifting','suspended load','falling object']): consequence='Potential fatal struck-by / crushing injury'
 elif contains(text,['fire','explosion','flammable']): consequence='Potential burn / fire / explosion fatality'
 elif contains(text,['height','fall','scaffold']): consequence='Potential serious/fatal fall'
 else: consequence='Potential serious injury or fatality depending on exposure'
 reasons=[]
 if risks: reasons.append(f'Detected {len(risks)} high-risk precursor signal(s).')
 if rules[0]!='Other / HSE Review': reasons.append('Matched one or more Life-Saving Rule categories.')
 if failure!='Requires HSE review': reasons.append('Narrative suggests a possible barrier/control failure.')
 return {'sif_class':cls,'sif_probability':min(.99,score/100),'priority_score':score,'life_saving_rules':rules,'activity':activity,'hazard':hazard,'barrier':barrier,'barrier_failure':failure,'potential_consequence':consequence,'reasons':reasons or ['No strong precursor signal detected.']}
