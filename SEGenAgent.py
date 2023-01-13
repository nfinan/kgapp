from whyis import autonomic
from rdflib import *
from slugify import slugify
from whyis import nanopub

sioc_types = Namespace("http://rdfs.org/sioc/types#")
sioc = Namespace("http://rdfs.org/sioc/ns#")
sio = Namespace("http://semanticscience.org/resource/")
dc = Namespace("http://purl.org/dc/terms/")
prov = autonomic.prov
whyis = autonomic.whyis

class SurfaceEnergyGen(autonomic.UpdateChangeService):
    activity_class = whyis.SurfaceEnergyGen

    def getInputClass(self):
        return sioc.Post

    def getOutputClass(self):
        return URIRef("http://purl.org/dc/dcmitype/Text")

    def get_query(self):
        return QUERY

    def process(self, i, o):
        content = i.value(sioc.content)
        # soup = BeautifulSoup(content, 'html.parser')
        # text = soup.get_text("\n")
        # o.add(URIRef("http://schema.org/text"), Literal(text))

QUERY = '''
PREFIX nm: <http://materialsmine.org/ns/>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?VolFrac ?Tg ?controlTg ?deltaTg (LCASE(?SurfaceTreatmentType) AS ?PST) (LCASE(?MatrixType) AS ?matrix) ?sample ?doi WHERE {
  ?sample a nm:PolymerNanocomposite;
          sio:hasComponentPart ?FillerPart ,
                               ?MatrixPart .
  
  ?doi sio:hasPart ?sample .

  ?FillerPart sio:hasRole [ a nm:Filler ] ;
              a [ rdfs:label "Silicon dioxide" ] ;
              sio:hasAttribute [ a nm:VolumeFraction ;
                                 sio:hasValue ?VolFrac ] .
  
  ?MatrixPart sio:hasRole [ a nm:Matrix ] ;
              a [ rdfs:label ?MatrixType ] .
  
  ?sample sio:hasAttribute [ a nm:GlassTransitionTemperature ;
                             sio:hasValue ?Tg ;
                             sio:hasUnit [ rdfs:label "Celsius" ] ] .
  

  ?controlsample sio:hasRole [ a sio:ControlRole ;
                               sio:inRelationTo ?sample ] ;
                 sio:hasAttribute [ a nm:GlassTransitionTemperature ;
                                    sio:hasValue ?controlTg ;
                                    sio:hasUnit [ rdfs:label "Celsius" ] ] .
  
  BIND ( ?Tg - ?controlTg AS ?deltaTg )
  
  OPTIONAL {
    ?FillerPart sio:isSurroundedBy [ sio:hasRole [ a nm:SurfaceTreatment ] ;
                                     a [ rdfs:label ?SurfaceTreatmentType ] ] .
  }                   
}
'''