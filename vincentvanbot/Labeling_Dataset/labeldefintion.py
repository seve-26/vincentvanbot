import ipdb
url_list = ['https://www.wga.hu/art/zzzarchi/13c/3/2/6padua12.jpg',
 'https://www.wga.hu/art/m/massys/quentin/2/ugly_duc.jpg',
 'https://www.wga.hu/art/r/rembrand/21portra/05portra.jpg',
 'https://www.wga.hu/art/m/mor/1maximi1.jpg',
 'https://www.wga.hu/art/p/ponzello/doria3.jpg',
 'https://www.wga.hu/art/c/canalett/g1/canalg10.jpg',
 'https://www.wga.hu/art/g/giovanni/rimini/life_chm.jpg',
 'https://www.wga.hu/art/zgothic/mosaics/5monreal/2transe4.jpg',
 'https://www.wga.hu/art/r/robbia/andrea/la_verna/3verna.jpg',
 'https://www.wga.hu/art/g/gericaul/1/105geric.jpg',
 'https://www.wga.hu/art/b/bellano/virgin.jpg',
 'https://www.wga.hu/art/b/bosch/5panels/11shipfo.jpg',
 'https://www.wga.hu/art/m/mostaert/jan/ador_mag.jpg',
 'https://www.wga.hu/art/l/loutherb/sh_wreck.jpg',
 'https://www.wga.hu/art/o/ochterve/s_musici.jpg',
 'https://www.wga.hu/art/t/tiepolo/gianbatt/5wurzbur/1hall2.jpg',
 'https://www.wga.hu/art/s/salimbe/various/mysticma.jpg',
 'https://www.wga.hu/art/h/holbein/hans_y/2drawing/1530/09meyer.jpg',
 'https://www.wga.hu/art/m/memling/1early2/04notri3.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/1451-500/2italia3/12religi.jpg',
 'https://www.wga.hu/art/h/halle/childsav.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/1401-450/2french/27religi.jpg',
 'https://www.wga.hu/art/c/canalett/8/canal8081.jpg',
 'https://www.wga.hu/art/w/wynants/riverlan.jpg',
 'https://www.wga.hu/art/c/cortona/2/5apollo3.jpg',
 'https://www.wga.hu/art/m/mantegna/02/sanluca2.jpg',
 'https://www.wga.hu/art/r/romano/p_medal1.jpg',
 'https://www.wga.hu/art/zzzarchi/14c/4/7glouce1.jpg',
 'https://www.wga.hu/art/p/predis/ambrogio/portram.jpg',
 'https://www.wga.hu/art/l/leonardo/12engine/3flying2.jpg',
 'https://www.wga.hu/art/w/wolgemut/dance_de.jpg',
 'https://www.wga.hu/art/r/rizzo/eve1.jpg',
 'https://www.wga.hu/art/g/grassi/viscont3.jpg',
 'https://www.wga.hu/art/m/master/zunk_ge/zunk_ge7/07angel.jpg',
 'https://www.wga.hu/art/g/gartner/berlinpa.jpg',
 'https://www.wga.hu/art/zzzarchi/12c/1/15g_1154.jpg',
 'https://www.wga.hu/art/l/leonardo/07study1/7leda1.jpg',
 'https://www.wga.hu/art/c/civitale/genova4.jpg',
 'https://www.wga.hu/art/g/gobert/ladyhebe.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/1251-300/1english/57englis.jpg',
 'https://www.wga.hu/art/d/delacroi/4/410delac.jpg',
 'https://www.wga.hu/art/c/cezanne/4/3lands05.jpg',
 'https://www.wga.hu/art/t/tiziano/08a/1ferra2c.jpg',
 'https://www.wga.hu/art/zzzarchi/17c/1/03g_1652.jpg',
 'https://www.wga.hu/art/m/master/zunk_du/2/abbot.jpg',
 'https://www.wga.hu/art/c/claesz/herrin.jpg',
 'https://www.wga.hu/art/e/eschwege/sintra2.jpg',
 'https://www.wga.hu/art/d/dossi/dosso/cosmas_d.jpg',
 'https://www.wga.hu/art/p/pontelli/sistina.jpg',
 'https://www.wga.hu/art/v/vonnoh/poppies.jpg']
url_list2 = ['https://www.wga.hu/art/o/oudry/father/huntstag.jpg',
 'https://www.wga.hu/art/b/bartolom/fruosino/desco1.jpg',
 'https://www.wga.hu/art/p/pomaranc/domitill.jpg',
 'https://www.wga.hu/art/j/juvarra/cristin1.jpg',
 'https://www.wga.hu/art/m/mantegna/07/2sposi08.jpg',
 'https://www.wga.hu/art/zzzarchi/16c/6/09b_1555.jpg',
 'https://www.wga.hu/art/p/pillemen/landwash.jpg',
 'https://www.wga.hu/art/u/urbani/vendra04.jpg',
 'https://www.wga.hu/art/m/master/zunk_ge/zunk_ge5/9print2.jpg',
 'https://www.wga.hu/art/p/premazzi/loggiai.jpg',
 'https://www.wga.hu/art/r/rubens/41portra/22sp1623.jpg',
 'https://www.wga.hu/art/c/chardin/2/08waterj.jpg',
 'https://www.wga.hu/art/zgothic/1romanes/cap-11c/24s_1002.jpg',
 'https://www.wga.hu/art/l/lorenzo/niccolo/coronati.jpg',
 'https://www.wga.hu/art/c/clodion/montesq1.jpg',
 'https://www.wga.hu/art/zgothic/mosaics/4palatin/25nave_s.jpg',
 'https://www.wga.hu/art/r/rosselin/bernardo/egidio1.jpg',
 'https://www.wga.hu/art/p/pellegri/1/pair1.jpg',
 'https://www.wga.hu/art/m/master/xunk_it/xunk_it2c/08galati.jpg',
 'https://www.wga.hu/art/s/seghers/daniel/garland.jpg',
 'https://www.wga.hu/art/b/borromin/agone2.jpg',
 'https://www.wga.hu/art/r/rembrand/53drawin/5/115stud.jpg',
 'https://www.wga.hu/art/b/bazille/08afterb.jpg',
 'https://www.wga.hu/art/a/antoine/monnaie2.jpg',
 'https://www.wga.hu/art/k/kobke/view_squ.jpg',
 'https://www.wga.hu/art/w/ward/escape.jpg',
 'https://www.wga.hu/art/l/leonardo/03/3litta.jpg',
 'https://www.wga.hu/art/w/weyden/rogier/14pieta/7lamenta.jpg',
 'https://www.wga.hu/art/b/bellini/giovanni/1480-89/2frari/134frar2.jpg',
 'https://www.wga.hu/art/c/covarrub/hospita3.jpg',
 'https://www.wga.hu/art/g/gozzoli/1early/06monte1.jpg',
 'https://www.wga.hu/art/c/cortona/2/3giove4a.jpg',
 'https://www.wga.hu/art/t/tintoret/3b/1albergo/1/03ceilin.jpg',
 'https://www.wga.hu/art/t/terborch/1/suitor.jpg',
 'https://www.wga.hu/art/r/rembrand/12passio/05passio.jpg',
 'https://www.wga.hu/art/s/signorel/various/4holyfam.jpg',
 'https://www.wga.hu/art/m/monet/01/early20.jpg',
 'https://www.wga.hu/art/p/pisano/nicola/1pisa_3.jpg',
 'https://www.wga.hu/art/u/utrecht/stillveg.jpg',
 'https://www.wga.hu/art/l/lopez/son2/goddess.jpg',
 'https://www.wga.hu/art/b/bernini/gianlore/zdrawing/selfpor1.jpg',
 'https://www.wga.hu/art/m/memling/2middle3/15novirg.jpg',
 'https://www.wga.hu/art/m/maulbert/01youth.jpg',
 'https://www.wga.hu/art/f/felici/percival.jpg',
 'https://www.wga.hu/art/f/francia/various/2crucif2.jpg',
 'https://www.wga.hu/art/a/albani/2/phaeton4.jpg',
 'https://www.wga.hu/art/c/coustou/guillaux/dauphin1.jpg',
 'https://www.wga.hu/art/g/greco_el/11/1102grec.jpg',
 'https://www.wga.hu/art/c/cellini/1/01salt.jpg',
 'https://www.wga.hu/art/c/ceresa/ladyhand.jpg',
 'https://www.wga.hu/art/zzdeco/1gold/08c/desider4.jpg',
 'https://www.wga.hu/art/c/covarrub/hospita4.jpg',
 'https://www.wga.hu/art/v/velazque/06/0603vela.jpg',
 'https://www.wga.hu/art/j/juan/1/lazarus3.jpg',
 'https://www.wga.hu/art/r/reynolds/serpents.jpg',
 'https://www.wga.hu/art/c/crosato/apollo.jpg',
 'https://www.wga.hu/art/m/maes/drummer.jpg',
 'https://www.wga.hu/art/r/ravestej/couple1.jpg',
 'https://www.wga.hu/art/l/lorenzet/pietro/2/15birth2.jpg',
 'https://www.wga.hu/art/a/arcimbol/5nature/042_128r.jpg',
 'https://www.wga.hu/art/t/toulouse/2/4misc02.jpg',
 'https://www.wga.hu/art/h/hackert/philipp/volturno.jpg',
 'https://www.wga.hu/art/m/master/pesaro/cecilia.jpg',
 'https://www.wga.hu/art/m/meckel/gasworks.jpg',
 'https://www.wga.hu/art/f/ferrari/gaudenzi/vercelli/2assunt2.jpg',
 'https://www.wga.hu/art/s/saftleve/herman/viewlinz.jpg',
 'https://www.wga.hu/art/a/andreani/triumph8.jpg',
 'https://www.wga.hu/art/c/cernotto/finding.jpg',
 'https://www.wga.hu/art/h/heda/ham_silv.jpg',
 'https://www.wga.hu/art/t/tibaldi/2/bologna2.jpg',
 'https://www.wga.hu/art/b/brown_ma/murray.jpg',
 'https://www.wga.hu/art/b/boullogn/louis_y/troyes1.jpg',
 'https://www.wga.hu/art/zzzarchi/14c/5/11s_1301.jpg',
 'https://www.wga.hu/art/k/kager/goldenha.jpg',
 'https://www.wga.hu/art/r/ricci/sebastia/1/venus_sa.jpg',
 'https://www.wga.hu/art/b/bury/countess.jpg',
 'https://www.wga.hu/art/m/macdonal/winchil.jpg',
 'https://www.wga.hu/art/r/raphael/7drawing/1/38study.jpg',
 'https://www.wga.hu/art/g/gossart/04religi/3adamev2.jpg',
 'https://www.wga.hu/art/g/gherardk/colonna4.jpg',
 'https://www.wga.hu/art/t/terborch/3/concers.jpg',
 'https://www.wga.hu/art/q/quercia/jacopo/bologna/ilaria_.jpg',
 'https://www.wga.hu/art/m/master/hausbuch/lamentat.jpg',
 'https://www.wga.hu/art/l/lorenzo/monaco/2/38monaco.jpg',
 'https://www.wga.hu/art/p/perugino/cambio/3famous2.jpg',
 'https://www.wga.hu/art/zgothic/gothic/1/01f_1230.jpg',
 'https://www.wga.hu/art/s/soldani/relief2.jpg',
 'https://www.wga.hu/art/b/baerz/dijon4.jpg',
 'https://www.wga.hu/art/s/sorgh/tavern.jpg',
 'https://www.wga.hu/art/m/master/zunk_du/1/triptyc2.jpg',
 'https://www.wga.hu/art/d/degas/5/1890s_06.jpg',
 'https://www.wga.hu/art/m/murillo/1/102muril.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/0651-700/2other/asburnh6.jpg',
 'https://www.wga.hu/art/m/metsu/1/pendant2.jpg',
 'https://www.wga.hu/art/c/chardin/2/07canary.jpg',
 'https://www.wga.hu/art/c/custodis/hynde1.jpg',
 'https://www.wga.hu/art/zzzarchi/16c/4/01e_1501.jpg',
 'https://www.wga.hu/art/c/caravagg/12/75stjohn.jpg',
 'https://www.wga.hu/art/r/rizzo/adam_eve.jpg',
 'https://www.wga.hu/art/l/longhena/4rezzon2.jpg']
url_list3 = ['https://www.wga.hu/art/g/gozzoli/2montefa/00scheme.jpg',
 'https://www.wga.hu/art/n/netscher/constant/mother_c.jpg',
 'https://www.wga.hu/art/b/bernini/gianlore/sculptur/1640/scipione.jpg',
 'https://www.wga.hu/art/e/eyck_van/jan/09ghent/2closed2/l4donor.jpg',
 'https://www.wga.hu/art/v/vos_m/anselmus.jpg',
 'https://www.wga.hu/art/b/buttafog/stanthon.jpg',
 'https://www.wga.hu/art/s/steen/page1/skittle.jpg',
 'https://www.wga.hu/art/zzzarchi/16c/4/02e_1502.jpg',
 'https://www.wga.hu/art/b/balen/feastacx.jpg',
 'https://www.wga.hu/art/a/amadeo/bergamo/facade1.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/1351-400/2italia/09herbal.jpg',
 'https://www.wga.hu/art/n/netscher/constant/portrait.jpg',
 'https://www.wga.hu/art/f/fontebas/1zenob09.jpg',
 'https://www.wga.hu/art/w/witz/c_cross.jpg',
 'https://www.wga.hu/art/d/duccio/maesta/verso_2/verso20b.jpg',
 'https://www.wga.hu/art/d/durer/2/13/4/079.jpg',
 'https://www.wga.hu/art/m/michelan/4drawing/10/03misc.jpg',
 'https://www.wga.hu/art/g/gossart/10print/06print.jpg',
 'https://www.wga.hu/art/l/lemmen/beach.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/1451-500/3flemis4/24flemis.jpg',
 'https://www.wga.hu/art/c/cuyp/aelbert/1/1timber.jpg',
 'https://www.wga.hu/art/zgothic/1romanes/po-12c21/16f_1134.jpg',
 'https://www.wga.hu/art/s/sorgh/akitchen.jpg',
 'https://www.wga.hu/art/s/sagot/cluny2.jpg',
 'https://www.wga.hu/art/p/perrault/colonna3.jpg',
 'https://www.wga.hu/art/j/jaersvel/goblet.jpg',
 'https://www.wga.hu/art/p/paolo/fei/virgin1.jpg',
 'https://www.wga.hu/art/c/cranach/lucas_e/08/3apollo2.jpg',
 'https://www.wga.hu/art/a/amadeo/bergamo/facade9.jpg',
 'https://www.wga.hu/art/r/rosselli/cosimo/lastsup3.jpg',
 'https://www.wga.hu/art/p/parmigia/3/judith.jpg',
 'https://www.wga.hu/art/m/meneghel/1altar61.jpg',
 'https://www.wga.hu/art/d/durer/2/12/7smallp/2/21_small.jpg',
 'https://www.wga.hu/art/p/piero/1/1miser02.jpg',
 'https://www.wga.hu/art/m/master/yunk_fr/yunk_fr1/16muff.jpg',
 'https://www.wga.hu/art/h/hals/dirk/banquet.jpg',
 'https://www.wga.hu/art/l/lemoyne/jeanloui/the_fear.jpg',
 'https://www.wga.hu/art/g/grebber/pieter/mother_c.jpg',
 'https://www.wga.hu/art/l/lamberti/niccolo/orsanmi3.jpg',
 'https://www.wga.hu/art/p/pajou/wailly1.jpg',
 'https://www.wga.hu/art/l/le_nain/visit.jpg',
 'https://www.wga.hu/art/v/velazque/02/0212vela.jpg',
 'https://www.wga.hu/art/b/boel/stil_owl.jpg',
 'https://www.wga.hu/art/m/master/xunk_it/xunk_it1/07sancta.jpg',
 'https://www.wga.hu/art/s/sarazin1/pol_leon.jpg',
 'https://www.wga.hu/art/a/angelico/07/panel2.jpg',
 'https://www.wga.hu/art/w/west/banks.jpg',
 'https://www.wga.hu/art/l/loth/good_sam.jpg',
 'https://www.wga.hu/art/m/madarasz/5dobozi.jpg',
 'https://www.wga.hu/art/b/bernini/gianlore/architec/ariccia4.jpg',
 'https://www.wga.hu/art/m/master/pesaro/crucifix.jpg',
 'https://www.wga.hu/art/w/wieringe/damiate.jpg',
 'https://www.wga.hu/art/a/altdorfe/3/4scenes2.jpg',
 'https://www.wga.hu/art/h/hamilto/philipp/pheasant.jpg',
 'https://www.wga.hu/art/t/tiepolo/gianbatt/2_1730s/12madon.jpg',
 'https://www.wga.hu/art/r/ryckaert/david3/astheold.jpg',
 'https://www.wga.hu/art/zzdeco/1gold/17c/05i_1601.jpg',
 'https://www.wga.hu/art/m/mirou/schwalb3.jpg',
 'https://www.wga.hu/art/c/coysevox/louis14a.jpg',
 'https://www.wga.hu/art/g/greuze/innocenx.jpg',
 'https://www.wga.hu/art/t/terborch/3/violinis.jpg',
 'https://www.wga.hu/art/p/porta1/tomaso/paul1.jpg',
 'https://www.wga.hu/art/e/eyck_van/jan/09ghent/1open3/l5pilgr.jpg',
 'https://www.wga.hu/art/c/court/womanlyi.jpg',
 'https://www.wga.hu/art/p/perino/z_aeneas.jpg',
 'https://www.wga.hu/art/o/osona/rodrigo2/shepherd.jpg',
 'https://www.wga.hu/art/b/brakenbu/mayqueen.jpg',
 'https://www.wga.hu/art/w/witz/stpeter1.jpg',
 'https://www.wga.hu/art/f/fuseli/05nightm.jpg',
 'https://www.wga.hu/art/m/masolino/brancacc/0view1.jpg',
 'https://www.wga.hu/art/g/gogh_van/02/nuenen04.jpg',
 'https://www.wga.hu/art/m/master/brunswic/calvary1.jpg',
 'https://www.wga.hu/art/r/richtera/crossing.jpg',
 'https://www.wga.hu/art/p/pesellin/sacracon.jpg',
 'https://www.wga.hu/art/b/bonanno/doors1.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/1401-450/6turin/14turin.jpg',
 'https://www.wga.hu/art/r/ravestey/stillif2.jpg',
 'https://www.wga.hu/art/zzzarchi/12c/2/1/24f_1103.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/1351-400/1french/french141.jpg',
 'https://www.wga.hu/art/a/angelico/09/cells/31_limbo.jpg',
 'https://www.wga.hu/art/d/duccio/maesta/0main/maest_04.jpg',
 'https://www.wga.hu/art/w/wesel/altar2.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/1301-350/3manesse/07maness.jpg',
 'https://www.wga.hu/art/zzzarchi/12c/2/3/07f_1151.jpg',
 'https://www.wga.hu/art/l/lens/regulus.jpg',
 'https://www.wga.hu/art/c/cranach/lucas_e/03/18jerome.jpg',
 'https://www.wga.hu/art/g/gauguin/03/4arles05.jpg',
 'https://www.wga.hu/art/zearly/1/1sculptu/capitals/6coptic1.jpg',
 'https://www.wga.hu/art/m/masolino/olona/25olona.jpg',
 'https://www.wga.hu/art/r/rocca/triumph.jpg',
 'https://www.wga.hu/art/f/flotner/venus.jpg',
 'https://www.wga.hu/art/a/albani/1/2summer.jpg',
 'https://www.wga.hu/art/r/rossi/cesi3.jpg',
 'https://www.wga.hu/art/c/cossiers/fortune1.jpg',
 'https://www.wga.hu/art/s/schlaun/3rusch1.jpg',
 'https://www.wga.hu/art/p/pater/fete_cha.jpg',
 'https://www.wga.hu/art/g/giotto/zz_misc/y_mosaic/12navice.jpg',
 'https://www.wga.hu/art/m/mijtens/jan/pompe.jpg',
 'https://www.wga.hu/art/c/carriera/leblond.jpg',
 'https://www.wga.hu/art/b/barbari/venus.jpg',
 'https://www.wga.hu/art/b/blanche/fathers.jpg',
 'https://www.wga.hu/art/z/zuccaro/federico/bologna.jpg',
 'https://www.wga.hu/art/v/vignola/andrea5.jpg',
 'https://www.wga.hu/art/s/stresor/oyster_d.jpg',
 'https://www.wga.hu/art/zzzarchi/12c/4/04e_1103.jpg',
 'https://www.wga.hu/art/c/cordierc/juivre1.jpg',
 'https://www.wga.hu/art/m/memberge/noahark4.jpg',
 'https://www.wga.hu/art/v/veronese/02a/1choir/1marcel2.jpg',
 'https://www.wga.hu/art/v/vittoria/2/dogepont.jpg',
 'https://www.wga.hu/art/c/claesz/goblet.jpg',
 'https://www.wga.hu/art/zzzarchi/11c/3/12i_1053.jpg',
 'https://www.wga.hu/art/d/drost/roman1.jpg',
 'https://www.wga.hu/art/m/mino/virgin_c.jpg',
 'https://www.wga.hu/art/r/rubens/41portra/09philos.jpg',
 'https://www.wga.hu/art/b/bruegel/pieter_e/08/02adorat.jpg',
 'https://www.wga.hu/art/b/botticel/90scenic/11calumn.jpg',
 'https://www.wga.hu/art/m/michelan/3sistina/1genesis/6adam/06_3ce6.jpg',
 'https://www.wga.hu/art/p/poelenbu/mercury.jpg',
 'https://www.wga.hu/art/s/sormanip/trellis.jpg',
 'https://www.wga.hu/art/l/la_hire/peace_ju.jpg',
 'https://www.wga.hu/art/d/degas/3/1870s_77.jpg',
 'https://www.wga.hu/art/m/millais/blindgir.jpg',
 'https://www.wga.hu/art/m/millet/02trussi.jpg',
 'https://www.wga.hu/art/c/canova/1/5magdale.jpg',
 'https://www.wga.hu/art/t/tiepolo/gianbatt/5wurzbur/4americ1.jpg',
 'https://www.wga.hu/art/h/hondecoe/melchior/peacock.jpg',
 'https://www.wga.hu/art/h/hals/frans/06-1643/54nopor2.jpg',
 'https://www.wga.hu/art/a/aelst/breakfas.jpg',
 'https://www.wga.hu/art/p/picart/stillif1.jpg',
 'https://www.wga.hu/art/zgothic/stained/12c/2/04rounde.jpg',
 'https://www.wga.hu/art/d/delacroi/3/309delac.jpg',
 'https://www.wga.hu/art/m/mena/virgin.jpg',
 'https://www.wga.hu/art/m/munkacsy/06munkac.jpg',
 'https://www.wga.hu/art/p/pacino/laudari2.jpg',
 'https://www.wga.hu/art/c/chernets/gallery.jpg',
 'https://www.wga.hu/art/m/master/flemalle/triptych/triptic1.jpg',
 'https://www.wga.hu/art/r/rodin/3busts/claudel1.jpg',
 'https://www.wga.hu/art/j/jacopo/cione/1/3r2_up1.jpg',
 'https://www.wga.hu/art/b/brouwer/smokingm.jpg',
 'https://www.wga.hu/art/b/bourdon/scene.jpg',
 'https://www.wga.hu/art/f/fabisch/beatrice.jpg',
 'https://www.wga.hu/art/z/zurbaran/1/shepherd.jpg',
 'https://www.wga.hu/art/zgothic/miniatur/1301-350/1english/73englis.jpg',
 'https://www.wga.hu/art/b/bortolin/cornar03.jpg',
 'https://www.wga.hu/art/l/lombardo/antonio/miracle.jpg',
 'https://www.wga.hu/art/q/quellin/jan/visitati.jpg',
 'https://www.wga.hu/art/k/kolbe/fanttree.jpg',
 'https://www.wga.hu/art/d/degas/3/1870s_80.jpg',
 'https://www.wga.hu/art/l/le_breto/cour1.jpg',
 'https://www.wga.hu/art/g/gerhard/fountain.jpg',
 'https://www.wga.hu/art/j/janneck/company.jpg',
 'https://www.wga.hu/art/d/dance/portanne.jpg',
 'https://www.wga.hu/art/b/binck/christi1.jpg',
 'https://www.wga.hu/art/v/veyrier/christ.jpg',
 'https://www.wga.hu/art/b/bassetti/adoratio.jpg',
 'https://www.wga.hu/art/n/nerocci/madonnc.jpg',
 'https://www.wga.hu/art/t/trautman/firescen.jpg',
 'https://www.wga.hu/art/zearly/1/1sculptu/various/6throne3.jpg',
 'https://www.wga.hu/art/t/tiziano/01_1510s/11padua1.jpg',
 'https://www.wga.hu/art/zzdeco/3furnitu/2/6g_1cupb.jpg',
 'https://www.wga.hu/art/f/fuseli/05nightx.jpg',
 'https://www.wga.hu/art/o/oudry/father/deadwolf.jpg',
 'https://www.wga.hu/art/t/terborch/2/woman_w.jpg',
 'https://www.wga.hu/art/s/savery/roelandt/crabfish.jpg',
 'https://www.wga.hu/art/m/master/honore/somme.jpg',
 'https://www.wga.hu/art/m/master/zunk_ge/zunk_ge8/04christ.jpg',
 'https://www.wga.hu/art/b/bentley/bentley5.jpg',
 'https://www.wga.hu/art/p/palamede/anthonie/officer.jpg',
 'https://www.wga.hu/art/l/lippi/filippo/1450pr/00view.jpg',
 'https://www.wga.hu/art/h/hildebr/christma.jpg',
 'https://www.wga.hu/art/d/durer/2/12/2apocaly/12apocal.jpg',
 'https://www.wga.hu/art/s/spiering/amadigi1.jpg',
 'https://www.wga.hu/art/a/andrea/castagno/1_1440s/08lasts9.jpg',
 'https://www.wga.hu/art/d/duccio/maesta/0main/maest_01c.jpg',
 'https://www.wga.hu/art/c/cortona/5/vialata2.jpg',
 'https://www.wga.hu/art/b/bosch/5panels/18mocked.jpg',
 'https://www.wga.hu/art/m/micheloz/1/2medici6.jpg',
 'https://www.wga.hu/art/c/coypel/noel/selfport.jpg',
 'https://www.wga.hu/art/s/sisley/2other/paris1.jpg',
 'https://www.wga.hu/art/n/nerocci/benedic3.jpg',
 'https://www.wga.hu/art/zzzarchi/13c/2/2/50f_1251.jpg',
 'https://www.wga.hu/art/m/memling/3mature3/25more1.jpg',
 'https://www.wga.hu/art/p/perronne/girl_kit.jpg',
 'https://www.wga.hu/art/r/rembrand/31landsc/07landsc.jpg',
 'https://www.wga.hu/art/zgothic/gothic/3a/2trade03.jpg',
 'https://www.wga.hu/art/t/turchi/lamentat.jpg',
 'https://www.wga.hu/art/m/michelan/1sculptu/medici/2lorenz41.jpg',
 'https://www.wga.hu/art/m/micheloz/2/pulpit.jpg',
 'https://www.wga.hu/art/r/ryckaert/david3/farm_int.jpg',
 'https://www.wga.hu/art/m/michelan/5archite/early/1lorenzo.jpg',
 'https://www.wga.hu/art/v/vellert/2triumph.jpg',
 'https://www.wga.hu/art/m/manet/4/4manet04.jpg',
 'https://www.wga.hu/art/l/lippi/flippino/carafa/2assump7.jpg',
 'https://www.wga.hu/art/p/pucelle/evreux5.jpg',
 'https://www.wga.hu/art/f/fontana/lavinia/jesusapp.jpg',
 'https://www.wga.hu/art/m/master/zunk_fl/graphics/interior.jpg',
 'https://www.wga.hu/art/s/sisley/2other/moret4.jpg',
 'https://www.wga.hu/art/g/giotto/z_panel/3polypty/10polypt.jpg',
 'https://www.wga.hu/art/d/duquesno/jerome2/tomb2.jpg',
 'https://www.wga.hu/art/r/rustici/baptist1.jpg']
dict_final = []


def detect_labels_uri(uri, n):
    """Detects labels in the file located in Google Cloud Storage or on the Web."""
    results = {}
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image, max_results=n)
    labels = response.label_annotations
    
    
    results = dict((label.description,1) for label in labels)
    return results

def mergeDict(dict1, dict2):
    ''' Merge dictionaries and keep values of common keys in list'''
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = value + dict1[key]
    return dict3

for i in range(200):
    dict_final.append(detect_labels_uri(url_list3[i],25))

final_final_dict = {}   

for dick in dict_final:
    final_final_dict = mergeDict(final_final_dict,dick)

#for label in labels: 
           # if results.has_key(label):
              #  results[label] += 1
           # else:
                #results[label] = 1
                

print (final_final_dict)

#print(detect_labels_uri('https://www.wga.hu/art/s/seghers/daniel/garland2.jpg',10))




