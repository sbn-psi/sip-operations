# SIP Operations

## Overview

These are tools that are used to generate delta-sips that are easier for the NSSDCA to process. This takes a SIP directory and removes all of the files that were present in a previous version of a SIP.

## Usage

`deltas.py --old_dir old_sip_dir --new_dir new_sip_dir --bundle_label bundle_gbo.ast.catalina.survey_v1.0.xml`

A directory called `deltas` will be created inside of `new_sip_dir`, which will contain only the differences between `old_sip_dir` and `new_sip_dir`.

## Requirements

BeautifulSoup4
lxml

## Current caveats

* This version currently only works for the Catalina Sky Survey. It should be possible to modify it to work with other bundles.
* The previous SIP needs to contain all previously submitted entries. (Or the deep-archive process needs to generate only relatively new entries, such as only the past month).

## See also

* PDS Deep Archive: https://nasa-pds.github.io/deep-archive/