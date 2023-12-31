# SIP Operations

## Overview

These are tools that are used to generate delta-sips that are easier for the NSSDCA to process. This takes a SIP directory and removes all of the files that were present in a previous version of a SIP. There is special handling for bundle and collection products:

* A bundle product is always included, since this is necessary for NSSDCA, and CSS is designed so that the bundle version does not increment.
* Only the latest version of a collection is included if there are multiple collections in a submisson. This reduces the number of redundant products that NSSDCA needs to ingest.

## Usage

### SIP delta generator

This is the primary script, which will find all of the products in the SIP/AIP files that haven't been submitted yet.

`deltas.py --old_dir old_sip_dir --new_dir new_sip_dir --bundle_label bundle_gbo.ast.catalina.survey_v1.0.xml`

`old_sip` dir may contain multiple SIP/AIP files. They will be combined into a single list of products to exclude. The SIP and transfer/checksum manifests should describe the same products, or *undefined behavior* will occur.

A directory called `deltas` will be created inside of `new_sip_dir`, which will contain only the differences between `old_sip_dir` and `new_sip_dir`.

### Checksum replacer

If you need to do a mass replacement of the checksums in the manifest, you can use `replace_checksums.py`.

`replace_checksums.py --sip sip_file --checksum ${CHECKSUM_FILE} --new_checksums new_checksums.txt`

### Label checksum updater

If you need to udpate the product labels after a manual update, you can use `update_label.py`.

`update_label.py --sip_dir sip_dir`

## Requirements

* BeautifulSoup4
* lxml

## Current caveats

* This version currently only works for the Catalina Sky Survey. It should be possible to modify it to work with other bundles.
* The previous SIP needs to contain all previously submitted entries. (Or the deep-archive process needs to generate only relatively new entries, such as only the past month).

## See also

* PDS Deep Archive: https://nasa-pds.github.io/deep-archive/