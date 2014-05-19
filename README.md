<h2>
<a name="RenrenDataRepo" class="anchor" href="#RenrenDataRepo"><span class="octicon octicon-link"></span></a>RenrenDataRepo</h2>
<p>a renren.com website based user datas capture and analysis project using python.
frends relation graph and public pages recommand...
thanks for help from</p><a href="https://github.com/yueyoum/renren-relationship">yueyoum/renren-relationship.</a>

<h2>
<a name="description" class="anchor" href="#description"><span class="octicon octicon-link"></span></a>1 description of the project</h2>

<p>using python to write a script, which can log in the</p> <a href="http://www.renren.com"><strong>renren website</strong></a><p>and obtain user datas for two purposes:
1 draw a relationship graph 2 recommend public pages</p>


<h2>
<a name="realization" class="anchor" href="#realization"><span class="octicon octicon-link"></span></a>2 realization of the project</h2>


<h3>
<a name="model 1" class="anchor" href="#model-1"><span class="octicon octicon-link"></span></a>2.1 part one: RenrenHandler</h3>
<p>In this part, we use some third part packages such as urllib, httplib2, re and json. Among these packages, urllib and httplib2 are used for log in the website and obtain datas, re is used for
matching strings with regular expression, and json is used for storage of object.
</p>

<h3>
<a name="model 2" class="anchor" href="#model-2"><span class="octicon octicon-link"></span></a>2.2 part two: dataVisualizationHandler</h3>
<p>In this part, we use some packages such as RenrenHandler and networkx. Among these packages, RenrenHandler is the user-define package we talked about above,
and networkx is a third part package used for drawing graphs.
</p>

<h3>
<a name="model 3" class="anchor" href="#model-3"><span class="octicon octicon-link"></span></a>2.3 part three: dataMiningHandler</h3>
<p>In this part, we use RenrenHandler and recommend public pages with</p>
<a href="http://en.m.wikipedia.org/wiki/K-nearest_neighbors_algorithm"><strong>KNN.</strong></a>


<h2>
<a name="presentation" class="anchor" href="#presentation"><span class="octicon octicon-link"></span></a>3 presentation</h2>
<h3>
	<p>console</p></h3>
&nbsp;&nbsp;&nbsp;&nbsp;<img src="./image/console.png" height="300" width="500" alt="console"></img>
<br><br><br><br>

<h3>
	<p>relationship-graph</p></h3>
&nbsp;&nbsp;&nbsp;&nbsp;<img src="./image/relationship-graph.png" height="300" width="500" alt="relationship-graph"></img>
<br><br><br><br>