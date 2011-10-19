
Commcare-HQ Overall project structure.

1.0_migration/
	Scripts which were used during the migration of some data from .9 to 1.0

apps/
	Django apps. The core of CCHQ. 
	
contrib/
	Holds locale or language settings, such as translations for the website.

docs/
	Some references which might be useful for developers. User-facing documentation rests in apps/docs/content

libs/
	Any third party libs (presumably python) that you'll need to reference
	
rapidsms/
	The utility we use to manage all SMS communications
	
scripts/
	Any helper scripts you'll want to write to deal with data and or other things.  This stuff should probably run outside the scope of the python environment
	
tests/
	Post deployment integration tests. Unit tests rest within the 'test' folder or file of individual apps.

utilities/
	Similar to scripts, with more of a focus on deployment utilities.
	
