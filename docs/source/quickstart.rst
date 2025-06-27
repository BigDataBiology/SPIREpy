Quickstart
==========


Python package
--------------

The Python package encapsulates the study and samples types from SPIRE into
classes with properties that allow you to access and interact with their data.
To load a study, we do:

.. code-block:: python

	from spirepy import Study

	study = Study("Lloyd-Price_2019_HMP2IBD")

We can then obtain the list of samples that belong to this study.

.. code-block:: python

	study.get_samples()  

The study's metadata:

.. code-block:: python
 
	study.get_metadata()

Or even the assembled genomes:

.. code-block:: python
 
	study.get_mags()

Likewise, many of these attributes and operations are parallel to samples
(:class:`spirepy.sample.Sample`) as well.

Command-line tool
-----------------

The command-line interface tool allows the interaction with data from SPIRE directly in the terminal. It possesses 2 main interfaces:

* `view`
* `download`

These 2 sub-commands allows us to print tables and download data from both studies and samples. For more information on the available commands use:

.. code-block:: bash
 
	spire --help

To view a study's metadata we can use:

.. code-block:: bash
 
	spire --study view metadata Lloyd-Price_2019_HMP2IBD

And to download the same table as a `.csv` file we can instead:

.. code-block:: bash
 
	spire --study download metadata Lloyd-Price_2019_HMP2IBD -o study/

