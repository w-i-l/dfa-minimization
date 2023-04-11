<h1>Deterministic finite automata minimization</h1>
<h2>An algorithm to convert a DFA to its minimal form</h2>
<img src='https://user-images.githubusercontent.com/65015373/231111594-55ef4181-4fba-4e5f-b28b-05ae0a8cf11e.png'>



<br>
<hr>
<h2>About it</h2>

<p>This project uses the classes from the <a href='https://github.com/w-i-l/deterministic-nondeterministic-finite-automata'>DFA implementation</a> with adjustments. The file format and the menu is similar to the first project.</p>


<br>
<hr>
<h2>How it works</h2>

<p>It uses the grouping algorithm to keep the equivalent states in the same subset.</p>
<p>First we split the states into two categories: final states and no final. From there we check if the next nodes from a given pair of nodes with a given letter will be in the same subset.</p>
<p>For more in depth explanation about the algorithm I suggest this videos:</p>
<ul>
    <li><a href='https://www.youtube.com/watch?v=0XaGAkY09Wc&ab_channel=NesoAcademy'>Minimization of DFA (Example 1)</a></li>
    <li><a href='https://www.youtube.com/watch?v=ex9sPLq5CRg&t=582s&ab_channel=NesoAcademy'>Minimization of DFA (Example 2)</a></li>
</ul>
