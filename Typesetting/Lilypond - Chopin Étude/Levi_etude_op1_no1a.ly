\version "2.18.2"
\header {
	title = \markup {
		\center-column {
			"Étude no 1 en préparation pour"
			"l'étude Op. 10 no 1 de Chopin"
		}
	}
	composer = "J. Levi, 1/2017"
}

upper = \relative c'' {
	\clef treble
	\tempo  "Moderato"

	{	% m 1
		\change Staff = "lower"
		\tweak Y-offset #2
		r8 
		-\tweak Y-offset #2
		\mp	
		\override Stem.direction = #UP
		c,, g' c
		\change Staff = "upper"
		e c g' c |
	}
	{	% m 2
		e c g c, e c
		\change Staff = "lower"
		g c, |
		\revert Stem.direction
	}
	{	% mm 3-4
		\tweak Y-offset #2
		r c a' c
		\change Staff = "upper"
		f c a' c | e c a c,
		\override Stem.direction = #UP
		d c 
		\change Staff = "lower"
		a c, |
	}
	{	% mm 5-6
		\revert Stem.direction
		\tweak Y-offset #2
		r b g' b
		\change Staff = "upper"
		d b g' b |
		d a fis c		
		\override Stem.direction = #UP
		d a
		\change Staff = "lower"
		fis c |
	}
	{	% m 7
		\revert Stem.direction
		\change Staff = "upper"
		\once \hide Rest r1_"[etc.]" |
	}
}

lower = \relative c {
	\clef bass
	<< 
		\new Voice = "first"
			  {c1~ | c }
		\new Voice = "second"
			\relative c, {c~\sustainOn | c }
	>>
	f,\sustainOff\sustainOn | %< f, f,>\sustainOff\sustainOn |
	< fis fis,>\sustainOff\sustainOn |
	\override Stem.direction = #DOWN
	<< g2 g,\sustainOff\sustainOn >>
	\revert Stem.direction
	<< fis'4 fis, >> < e' e, > | << d1 d,\sustainOff\sustainOn >> |
	< g' g, >\sustainOff\sustainOn |
}

\score {
	\new PianoStaff <<
	\time 4/4
	    \set PianoStaff.instrumentName = #"Piano  "
	    \new Staff = "upper" \upper
	    \new Staff = "lower" \lower
	>>
  \layout {
		\override TextSpanner.bound-details.left.text
  		 = \markup { \italic legato }
	}
}

