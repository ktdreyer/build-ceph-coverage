# vim: set noexpandtab ts=8 sw=8 :
#
# spec file for package ceph
#
# Copyright (C) 2004-2017 The Ceph Project Developers. See COPYING file
# at the top-level directory of this distribution and at
# https://github.com/ceph/ceph/blob/master/COPYING
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon.
#
# This file is under the GNU Lesser General Public License, version 2.1
#
# Please submit bugfixes or comments via http://tracker.ceph.com/
#
%bcond_without ocf
%bcond_without cephfs_java
%if 0%{?suse_version}
%bcond_with ceph_test_package
%else
%bcond_without ceph_test_package
%endif
%bcond_with make_check
%ifarch s390 s390x
%bcond_with tcmalloc
%else
%bcond_without tcmalloc
%endif
%bcond_with lowmem_builder
%if 0%{?fedora} || 0%{?rhel}
%bcond_without selinux
%endif
%if 0%{?suse_version}
%bcond_with selinux
%endif

# LTTng-UST enabled on Fedora, RHEL 6+, and SLE (not openSUSE)
%if 0%{?fedora} || 0%{?rhel} >= 6 || 0%{?suse_version}
%if ! 0%{?is_opensuse}
%bcond_without lttng
%endif
%endif

%if %{with selinux}
# get selinux policy version
%{!?_selinux_policy_version: %global _selinux_policy_version %(sed -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp 2>/dev/null || echo 0.0.0)}
%endif

%global _hardened_build 1

%{!?_udevrulesdir: %global _udevrulesdir /lib/udev/rules.d}
%{!?tmpfiles_create: %global tmpfiles_create systemd-tmpfiles --create}
%{!?python3_pkgversion: %global python3_pkgversion 3}

# unify libexec for all targets
%global _libexecdir %{_exec_prefix}/lib


#################################################################################
# main package definition
#################################################################################
Name:		ceph
Version:	12.2.5
Release:	59%{?dist}
%if 0%{?fedora} || 0%{?rhel}
Epoch:		2
%endif

# define _epoch_prefix macro which will expand to the empty string if epoch is
# undefined
%global _epoch_prefix %{?epoch:%{epoch}:}

Summary:	User space components of the Ceph file system
License:	LGPL-2.1 and CC-BY-SA-3.0 and GPL-2.0 and BSL-1.0 and BSD-3-Clause and MIT
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
URL:		http://ceph.com/
Source0:	https://download.ceph.com/tarballs/%{name}-%{version}.tar.gz

Patch0001: 0001-fuse-handle-errors-appropriately-when-getting-group-.patch
Patch0002: 0002-client-remove-init_groups.patch
Patch0003: 0003-client-have-init_gids-just-set-alloced_gids-to-true.patch
Patch0004: 0004-client-remove-_getgrouplist.patch
Patch0005: 0005-client-remove-getgroups_cb.patch
Patch0006: 0006-fuse-wire-up-fuse_ll_access.patch
Patch0007: 0007-mds-add-asok-command-that-dumps-metadata-popularity.patch
Patch0008: 0008-Make-MDS-evaluates-the-overload-situation-with-the-s.patch
Patch0009: 0009-simplify-mds-overload-judgement-logic.patch
Patch0010: 0010-mds-fix-request-rate-calculation.patch
Patch0011: 0011-mds-adjust-subtree-popularity-after-rename.patch
Patch0012: 0012-mds-remove-unused-MDBalancer-export_empties.patch
Patch0013: 0013-mds-always-pass-current-time-to-MDBalancer-hit_inode.patch
Patch0014: 0014-mds-cleanup-MDBalancer-try_rebalance.patch
Patch0015: 0015-mds-don-t-try-exporting-dirfrags-under-mds-s-own-mds.patch
Patch0016: 0016-mds-don-t-try-exporting-subdir-if-dirfrag-is-already.patch
Patch0017: 0017-mds-mds-optimize-MDBalancer-try_rebalance.patch
Patch0018: 0018-mds-avoid-creating-unnecessary-subtrees-during-load-.patch
Patch0019: 0019-mds-optimize-MDBalancer-find_exports.patch
Patch0020: 0020-mds-check-export-pin-when-choosing-dirfrags-for-expo.patch
Patch0021: 0021-mds-cleanup-mds_load-map-access-update.patch
Patch0022: 0022-mds-calculate-other-mds-last_epoch_under-locally.patch
Patch0023: 0023-mds-add-list-to-track-recently-used-sub-directories.patch
Patch0024: 0024-mds-limit-run-time-of-load-balancer.patch
Patch0025: 0025-client-add-ceph_ll_sync_inode.patch
Patch0026: 0026-client-flush-the-mdlog-in-_fsync-before-waiting-on-u.patch
Patch0027: 0027-rgw-fix-use-of-libcurl-with-empty-header-values.patch
Patch0028: 0028-rgw-add-buffering-filter-to-compression-for-fetch_re.patch
Patch0029: 0029-rgw-fix-bi_list-to-reset-is_truncated-flag-if-it-ski.patch
Patch0030: 0030-rgw-raise-log-level-on-coroutine-shutdown-errors.patch
Patch0031: 0031-ceph-disk-default-to-filestore.patch
Patch0032: 0032-rgw-consolidate-code-that-implements-hashing-algorit.patch
Patch0033: 0033-rgw-ability-to-list-bucket-contents-in-unsorted-orde.patch
Patch0034: 0034-rgw-Cache-notify-fault-injection.patch
Patch0035: 0035-rgw-Robustly-notify.patch
Patch0036: 0036-osd-Move-creation-of-master_set-to-scrub_compare_map.patch
Patch0037: 0037-osd-Warn-about-objects-with-too-many-omap-entries.patch
Patch0038: 0038-osd-Add-a-flag-to-ScrubMap-to-signal-check-needed.patch
Patch0039: 0039-qa-workunits-rados-test_large_omap_detection-Scrub-p.patch
Patch0040: 0040-mon-PGMap-Summarise-OSDs-in-blocked-stuck-requests.patch
Patch0041: 0041-ceph_volume_client-allow-volumes-without-namespace-i.patch
Patch0042: 0042-qa-ignore-version-in-auth-metadata-comp.patch
Patch0043: 0043-rgw-RGWRadosGetOmapKeysCR-uses-completion-return-cod.patch
Patch0044: 0044-rgw-RGWRadosGetOmapKeysCR-uses-omap_get_keys2.patch
Patch0045: 0045-rgw-add-lagging-shard-ids-in-rgw-sync-status.patch
Patch0046: 0046-rgw-display-errors-of-object-sync-failed-in-sync-err.patch
Patch0047: 0047-rgw-add-RGWReadDataSyncRecoveringShardsCR-to-read-re.patch
Patch0048: 0048-rgw-display-data-sync-recovering-shards-in-radosgw-a.patch
Patch0049: 0049-rgw-read-behind-bucket-shards-of-a-specified-data-lo.patch
Patch0050: 0050-rgw-add-shard-id-for-data-sync-status.patch
Patch0051: 0051-doc-update-radosgw-admin.rst-and-help.t-about-data-s.patch
Patch0052: 0052-rgw-translate-the-state-in-rgw_data_sync_marker.patch
Patch0053: 0053-radosgw-admin-rename-bucket-sync-status-to-bucket-sy.patch
Patch0054: 0054-rgw-rgw_bucket_sync_status-takes-bucket-info.patch
Patch0055: 0055-rgw-expose-struct-bucket_index_marker_info-in-header.patch
Patch0056: 0056-radosgw-admin-add-pretty-bucket-sync-status-command.patch
Patch0057: 0057-rgw-admin-support-for-processing-all-gc-objects-incl.patch
Patch0058: 0058-rgw-use-aio-for-gc-processing.patch
Patch0059: 0059-rgw-use-a-single-gc-io-manager-for-all-shards.patch
Patch0060: 0060-rgw-trim-gc-index-using-aio.patch
Patch0061: 0061-rgw-make-gc-concurrenct-io-size-configurable.patch
Patch0062: 0062-rgw-gc-aio-replace-lists-with-other-types.patch
Patch0063: 0063-rgw-use-vector-for-remove_tags-in-gc-aio.patch
Patch0064: 0064-qa-restful-Test-pg_num-pgp_num-modifications.patch
Patch0065: 0065-restful-Support-auid-pool-argument.patch
Patch0066: 0066-restful-Set-the-value-of-the-argument.patch
Patch0067: 0067-restful-Fix-jsonification.patch
Patch0068: 0068-prometheus-Fix-prometheus-shutdown-restart.patch
Patch0069: 0069-prometheus-Handle-the-TIME-perf-counter-type-metrics.patch
Patch0070: 0070-mgr-Expose-pg_sum-in-pg_summary.patch
Patch0071: 0071-prometheus-Expose-number-of-degraded-misplaced-unfou.patch
Patch0072: 0072-pybind-mgr-prometheus-unify-label-names-move-away-fr.patch
Patch0073: 0073-doc-mgr-prometheus-add-instructions-to-correlate-met.patch
Patch0074: 0074-mds-check-for-session-import-race.patch
Patch0075: 0075-mds-handle-imported-session-race.patch
Patch0076: 0076-qa-backport-helper-functions.patch
Patch0077: 0077-qa-get-status-to-handle-older-api.patch
Patch0078: 0078-mds-don-t-discover-inode-dirfrag-when-mds-is-in-star.patch
Patch0079: 0079-mds-properly-check-auth-subtree-count-in-MDCache-shu.patch
Patch0080: 0080-mds-kick-rdlock-if-waiting-for-dirfragtreelock.patch
Patch0081: 0081-client-don-t-hang-when-MDS-sessions-are-evicted.patch
Patch0082: 0082-qa-tasks-allow-custom-timeout-for-umount_wait.patch
Patch0083: 0083-qa-cephfs-test-if-evicted-client-unmounts-without-ha.patch
Patch0084: 0084-rgw-require-yes-i-really-mean-it-to-run-radosgw-admi.patch
Patch0085: 0085-prometheus-Fix-order-of-occupation-values.patch
Patch0086: 0086-selinux-Allow-ceph-to-execute-ldconfig.patch
Patch0087: 0087-selinux-Allow-ceph-to-block-suspend.patch
Patch0088: 0088-osd-osd_types-fix-object_stat_sum_t-decode.patch
Patch0089: 0089-msg-async-simple-include-MGR-as-service-when-applyin.patch
Patch0090: 0090-include-ceph_features-define-CEPHX2-feature.patch
Patch0091: 0091-auth-cephx-CephxSessionHandler-implement-CEPHX_V2-ca.patch
Patch0092: 0092-mon-msg-implement-cephx_-_require_version-options.patch
Patch0093: 0093-auth-cephx-add-authorizer-challenge.patch
Patch0094: 0094-cephx-update-docs.patch
Patch0095: 0095-auth-cephx-CephxProtocol-better-random.patch
Patch0096: 0096-rgw-add-configurable-AWS-compat-invalid-range-get-be.patch
Patch0097: 0097-filestore-Raise-the-priority-of-two-counters.patch
Patch0098: 0098-mgr-Expose-avgcount-for-long-running-avgs.patch
Patch0099: 0099-mgr_module-Deal-with-long-running-avgs-properly.patch
Patch0100: 0100-prometheus-Expose-sum-count-pairs-for-avgs.patch
Patch0101: 0101-doc-prometheus-Mention-the-long-running-avg-types.patch
Patch0102: 0102-mds-avoid-calling-rejoin_gather_finish-two-times-suc.patch
Patch0103: 0103-mds-tighten-conditions-of-calling-rejoin_gather_fini.patch
Patch0104: 0104-osdc-ObjectCacher-allow-discard-to-complete-in-fligh.patch
Patch0105: 0105-client-avoid-freeing-inode-when-it-contains-TX-buffe.patch
Patch0106: 0106-qa-test-for-trim_caps-segfault-for-trimmed-dentries.patch
Patch0107: 0107-client-delay-dentry-trimming-until-after-cap-travers.patch
Patch0108: 0108-librbd-commit-IO-as-safe-when-complete-if-writeback-.patch
Patch0109: 0109-rgw-ObjectCache-put-avoids-separate-find-insert.patch
Patch0110: 0110-rgw-update-ObjectCacheInfo-time_added-on-overwrite.patch
Patch0111: 0111-rgw-aws4-auth-supports-PutBucketRequestPayment.patch
Patch0112: 0112-mgr-expose-avg-data-for-long-running-avgs.patch
Patch0113: 0113-test-rgw-test-incremental-sync-of-acls-on-versioned-.patch
Patch0114: 0114-rgw-Object-Write-_do_write_meta-takes-optional-olh-e.patch
Patch0115: 0115-rgw-fetch_remote_obj-takes-optional-olh-epoch.patch
Patch0116: 0116-rgw-fetch_remote_obj-applies-olh-even-if-object-is-c.patch
Patch0117: 0117-rgw-SyncModule-sync_object-takes-optional-olh-epoch.patch
Patch0118: 0118-rgw-bucket-sync-only-provides-an-epoch-for-olh-opera.patch
Patch0119: 0119-rgw-bucket-sync-doesn-t-squash-over-olh-entries.patch
Patch0120: 0120-rgw-bucket-sync-allows-OP_ADD-on-versioned-objects.patch
Patch0121: 0121-rgw-CompleteMultipart-applies-its-olh_epoch.patch
Patch0122: 0122-rgw-bucket-sync-updates-high-marker-for-squashed-ent.patch
Patch0123: 0123-rgw-bucket-sync-only-allows-one-olh-op-at-a-time.patch
Patch0124: 0124-rgw-Silence-maybe-uninitialized-false-positives.patch
Patch0125: 0125-mon-OSDMonitor-enforce-caps-when-creating-deleting-u.patch
Patch0126: 0126-mon-OSDMonitor-enforce-caps-for-all-remaining-pool-o.patch
Patch0127: 0127-pybind-rados-new-methods-for-manipulating-self-manag.patch
Patch0128: 0128-qa-workunits-rbd-test-self-managed-snapshot-create-r.patch
Patch0129: 0129-qa-workunits-rados-test-pool-op-permissions.patch
Patch0130: 0130-osd-filestore-Change-default-filestore_merge_thresho.patch
Patch0131: 0131-osd-PrimaryLogPG-rebuild-attrs-from-clients.patch
Patch0132: 0132-mon-MDSMonitor-do-not-send-redundant-MDS-health-mess.patch
Patch0133: 0133-mds-combine-MDCache-cap_exports-cap_export_targets.patch
Patch0134: 0134-mds-don-t-add-blacklisted-clients-to-reconnect-gathe.patch
Patch0135: 0135-mds-filter-out-blacklisted-clients-when-importing-ca.patch
Patch0136: 0136-mds-properly-reconnect-client-caps-after-loading-ino.patch
Patch0137: 0137-client-fix-race-in-concurrent-readdir.patch
Patch0138: 0138-client-invalidate-caps-and-leases-when-session-becom.patch
Patch0139: 0139-qa-tasks-cephfs-add-test-for-renewing-stale-session.patch
Patch0140: 0140-mds-set-could_consume-to-false-when-no-purge-queue-i.patch
Patch0141: 0141-mds-reply-session-reject-for-open-request-from-black.patch
Patch0142: 0142-qa-tasks-cephfs-add-timeout-parameter-to-kclient-umo.patch
Patch0143: 0143-client-fix-issue-of-revoking-non-auth-caps.patch
Patch0144: 0144-mds-properly-trim-log-segments-after-scrub-repairs-s.patch
Patch0145: 0145-mds-fix-some-memory-leak.patch
Patch0146: 0146-mds-fix-leak-of-MDSCacheObject-waiting.patch
Patch0147: 0147-mds-include-nfiles-nsubdirs-of-directory-inode-in-MC.patch
Patch0148: 0148-common-DecayCounter-set-last_decay-to-current-time-w.patch
Patch0149: 0149-mds-send-cap-export-message-when-exporting-non-auth-.patch
Patch0150: 0150-mds-don-t-report-slow-request-for-blocked-filelock-r.patch
Patch0151: 0151-mds-fix-occasional-dir-rstat-inconsistency-between-m.patch
Patch0152: 0152-client-update-inode-fields-according-to-issued-caps.patch
Patch0153: 0153-ceph-disk-revise-the-help-message-for-prepare-comman.patch
Patch0154: 0154-Allow-swift-acls-to-be-deleted.patch
Patch0155: 0155-prometheus-Fix-metric-resets.patch
Patch0156: 0156-prometheus-Make-the-cache-timeout-configurable.patch
Patch0157: 0157-prometheus-Use-instance-instead-of-inst-variable.patch
Patch0158: 0158-prometheus-Optimize-metrics-formatting.patch
Patch0159: 0159-prometheus-Remove-the-Metrics-class.patch
Patch0160: 0160-prometheus-Format-metrics-in-the-collect-function.patch
Patch0161: 0161-prometheus-Reset-the-time-the-data-was-captured.patch
Patch0162: 0162-prometheus-Set-the-response-header-for-cached-respon.patch
Patch0163: 0163-rgw-add-option-for-relaxed-region-enforcement.patch
Patch0164: 0164-rgw-change-default-rgw_thread_pool_size-to-512.patch
Patch0165: 0165-rgw-do-not-ignore-EEXIST-in-RGWPutObj-execute.patch
Patch0166: 0166-radosgw-admin-sync-error-trim-loops-until-complete.patch
Patch0167: 0167-rgw-add-curl_low_speed_limit-and-curl_low_speed_time.patch
Patch0168: 0168-rgw-fix-gc-may-cause-a-large-number-of-read-traffic.patch
Patch0169: 0169-rgw-set-default-objecter_inflight_ops-24576.patch
Patch0170: 0170-rgw-fix-index-update-in-dir_suggest_changes.patch
Patch0171: 0171-rgw-continue-enoent-index-in-dir_suggest.patch
Patch0172: 0172-ceph-volume-Restore-SELinux-context.patch
Patch0173: 0173-mon-OSDMonitor-Warn-when-expected_num_objects-will-h.patch
Patch0174: 0174-mon-OSDMonitor-Warn-if-missing-expected_num_objects.patch
Patch0175: 0175-mds-print-mdsmap-processed-at-low-debug-level.patch
Patch0176: 0176-mds-dump-recent-events-on-respawn.patch
Patch0177: 0177-mds-increase-debug-level-for-dropped-client-cap-msg.patch
Patch0178: 0178-mds-avoid-traversing-all-dirfrags-when-trying-to-get.patch
Patch0179: 0179-mds-introduce-MDSMap-get_mds_set_lower_bound.patch
Patch0180: 0180-mds-handle-discontinuous-mdsmap.patch
Patch0181: 0181-qa-tasks-cephfs-add-test-for-discontinuous-mdsmap.patch
Patch0182: 0182-mds-update-MDSRank-cluster_degraded-before-handling-.patch
Patch0183: 0183-luminous-mgr-MgrClient-Protect-daemon_health_metrics.patch
Patch0184: 0184-rgw-raise-default-rgw_curl_low_speed_time-to-300-sec.patch
Patch0185: 0185-rgw-fix-injectargs-for-objecter_inflight_ops.patch
Patch0186: 0186-mds-fix-unhealth-heartbeat-during-rejoin.patch
Patch0187: 0187-mds-mark-beacons-as-high-priority.patch
Patch0188: 0188-MDSMonitor-cleanup-and-protect-fsmap-access.patch
Patch0189: 0189-mon-fix-standby-replay-in-multimds-setup.patch
Patch0190: 0190-mon-respect-standby_for_fscid-when-choosing-standby-.patch
Patch0191: 0191-mds-move-compat-set-methods-to-MDSMap.patch
Patch0192: 0192-mds-refactor-Filesystem-init.patch
Patch0193: 0193-mds-refactor-FSMap-init.patch
Patch0194: 0194-mds-refactor-MDSMap-init.patch
Patch0195: 0195-MDSMonitor-refactor-last_beacons-to-use-mono_clock.patch
Patch0196: 0196-MDSMonitor-clean-up-use-of-pending-fsmap-in-uncommit.patch
Patch0197: 0197-MDSMonitor-note-beacons-and-cluster-changes-at-low-d.patch
Patch0198: 0198-mds-report-lagginess-at-lower-debug.patch
Patch0199: 0199-mds-use-fast-dispatch-to-handle-MDSBeacon.patch
Patch0200: 0200-MDSMonitor-fix-compile-error.patch
Patch0201: 0201-msg-lower-verbosity-on-normal-event.patch
Patch0202: 0202-mon-test-if-gid-exists-in-pending-for-prepare_beacon.patch
Patch0203: 0203-mds-print-is_laggy-message-once.patch
Patch0204: 0204-osd-increase-default-hard-pg-limit.patch
Patch0205: 0205-osd-mon-increase-mon_max_pg_per_osd-to-250.patch
Patch0206: 0206-luminous-osd-change-log-level-when-withholding-pg-cr.patch
Patch0207: 0207-mds-hold-slave-request-refernce-when-dumping-MDReque.patch
Patch0208: 0208-mds-don-t-modify-filepath-when-printing.patch
Patch0209: 0209-mds-cleanup-CDir-freezing-frozen-tree-check.patch
Patch0210: 0210-mds-more-description-for-failed-authpin.patch
Patch0211: 0211-client-check-for-unmounted-condition-before-printing.patch
Patch0212: 0212-ceph_volume_client-add-delay-for-MDSMap-to-be-distri.patch
Patch0213: 0213-mds-avoid-using-g_conf-get_val-.-.-in-hot-path.patch
Patch0214: 0214-mds-health-warning-for-slow-metadata-IO.patch
Patch0215: 0215-mds-improve-error-handling-in-PurgeQueue.patch
Patch0216: 0216-mds-cleanup-MDSRank-evict_client.patch
Patch0217: 0217-librbd-fix-refuse-to-release-lock-when-cookie-is-the.patch
Patch0218: 0218-librbd-utilize-the-journal-disabled-policy-when-remo.patch
Patch0219: 0219-osd-PG-do-not-blindly-roll-forward-to-log.head.patch
Patch0220: 0220-qa-standalone-osd-repro_long_log.sh-fix-test.patch
Patch0221: 0221-qa-standalone-osd-ec-error-rollforward-reproduce-bug.patch
Patch0222: 0222-client-retry-remount-on-dcache-invalidation-failure.patch
Patch0223: 0223-rgw-raise-debug-level-on-redundant-data-sync-error-m.patch
Patch0224: 0224-rgw-optimize-function-abort_bucket_multiparts.patch
Patch0225: 0225-rgw-abort_bucket_multiparts-ignores-individual-NoSuc.patch
Patch0226: 0226-msg-set-O_NONBLOCK-on-file-status-flags.patch
Patch0227: 0227-set-missing-CLOEXEC-on-opened-fds.patch
Patch0228: 0228-rgw-fix-chunked-encoding-for-chunks-1MiB.patch
Patch0229: 0229-rgw-enable-override-of-tcmalloc-linkage.patch
Patch0230: 0230-rgw-making-implicit_tenants-backwards-compatible.patch
Patch0231: 0231-rgw-RGWBucket-link-supports-tenant.patch
Patch0232: 0232-Add-several-types-to-ceph-dencoder.patch
Patch0233: 0233-Add-bucket-new-name-option-to-radosgw-admin.patch
Patch0234: 0234-rgw-bucket-link-Add-ability-to-name-bucket-w-differe.patch
Patch0235: 0235-rgw-bucket-link-simplify-use-of-get-bucket-info.patch
Patch0236: 0236-rgw-bucket-link-use-data-from-bucket_info-to-rewrite.patch
Patch0237: 0237-rearrange-simplify-RGWBucket-link-logic-start-bucket.patch
Patch0238: 0238-rgw-bucket-link-base-bucket-move-tenant-id-only.patch
Patch0239: 0239-rgw-bucket-link-bucket-move-handle-bucket-names-too.patch
Patch0240: 0240-rgw-bucket-link-bucket-move-documentation-changes.patch
Patch0241: 0241-mon-HealthMonitor-do-not-send-MMonHealthChecks-to-pr.patch
Patch0242: 0242-osd-OSDMap-add-SIGNIFICANT_FEATURES-and-helper.patch
Patch0243: 0243-mon-OSDMonitor-move-OSDMap-feature-calculation-into-.patch
Patch0244: 0244-mon-OSDMonitor-add-feature-into-osdmap-cache-key.patch
Patch0245: 0245-messages-MOSDMap-significant-feature-bits.patch
Patch0246: 0246-crush-CrushWrapper-clean-up-member-init.patch
Patch0247: 0247-osd-OSDMap-CRUSH_TUNABLES5-added-in-jewel-not-kraken.patch
Patch0248: 0248-rgw-copy-actual-stats-from-the-source-shards-during-.patch
Patch0249: 0249-mds-simplify-beacon-init.patch
Patch0250: 0250-mds-use-monotonic-clock-in-beacon.patch
Patch0251: 0251-mds-use-monotonic-waits-in-Beacon.patch
Patch0252: 0252-rgw-remove-redundant-quota-logic-from-admin-user-api.patch
Patch0253: 0253-rgw-add-helper-functions-to-apply-configured-default.patch
Patch0254: 0254-rgw-RemoteApplier-create_account-applies-default-quo.patch
Patch0255: 0255-luminous-filestore-add-pgid-in-filestore-pg-dir-spli.patch

%if 0%{?suse_version}
%if 0%{?is_opensuse}
ExclusiveArch:  x86_64 aarch64 ppc64 ppc64le
%else
ExclusiveArch:  x86_64 aarch64 ppc64le s390x
%endif
%endif
#################################################################################
# dependencies that apply across all distro families
#################################################################################
Requires:       ceph-osd = %{_epoch_prefix}%{version}-%{release}
Requires:       ceph-mds = %{_epoch_prefix}%{version}-%{release}
Requires:       ceph-mgr = %{_epoch_prefix}%{version}-%{release}
Requires:       ceph-mon = %{_epoch_prefix}%{version}-%{release}
Requires(post):	binutils
%if 0%{with cephfs_java}
BuildRequires:	java-devel
BuildRequires:	sharutils
%endif
%if 0%{with selinux}
BuildRequires:	checkpolicy
BuildRequires:	selinux-policy-devel
BuildRequires:	/usr/share/selinux/devel/policyhelp
%endif
%if 0%{with make_check}
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	python-cherrypy
BuildRequires:	python-werkzeug
%endif
%if 0%{?suse_version}
BuildRequires:	python-CherryPy
BuildRequires:	python-Werkzeug
BuildRequires:	python-numpy-devel
%endif
BuildRequires:  python-coverage
BuildRequires:	python-pecan
BuildRequires:	socat
%endif
BuildRequires:	bc
BuildRequires:	gperf
BuildRequires:  cmake
BuildRequires:	cryptsetup
BuildRequires:	fuse-devel
BuildRequires:	gcc-c++
BuildRequires:	gdbm
%if 0%{with tcmalloc}
BuildRequires:	gperftools-devel >= 2.4
%endif
BuildRequires:  jq
BuildRequires:	leveldb-devel > 1.2
BuildRequires:	libaio-devel
BuildRequires:	libblkid-devel >= 2.17
BuildRequires:	libcurl-devel
BuildRequires:	libudev-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	make
BuildRequires:	parted
BuildRequires:	perl
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	python-nose
BuildRequires:	python-requests
BuildRequires:	python-virtualenv
BuildRequires:	snappy-devel
BuildRequires:	udev
BuildRequires:	util-linux
BuildRequires:	valgrind-devel
BuildRequires:	which
BuildRequires:	xfsprogs
BuildRequires:	xfsprogs-devel
BuildRequires:	xmlstarlet
BuildRequires:	yasm

#################################################################################
# distro-conditional dependencies
#################################################################################
%if 0%{?suse_version}
BuildRequires:  pkgconfig(systemd)
BuildRequires:	systemd-rpm-macros
BuildRequires:	systemd
%{?systemd_requires}
PreReq:		%fillup_prereq
BuildRequires:	net-tools
BuildRequires:	libbz2-devel
BuildRequires:  btrfsprogs
BuildRequires:	mozilla-nss-devel
BuildRequires:	keyutils-devel
BuildRequires:  libopenssl-devel
BuildRequires:  lsb-release
BuildRequires:  openldap2-devel
BuildRequires:	python-Cython
BuildRequires:	python-PrettyTable
BuildRequires:	python-Sphinx
BuildRequires:  rdma-core-devel
%endif
%if 0%{?fedora} || 0%{?rhel}
Requires:	systemd
BuildRequires:  boost-random
BuildRequires:	btrfs-progs
BuildRequires:	nss-devel
BuildRequires:	keyutils-libs-devel
BuildRequires:	libibverbs-devel
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel
BuildRequires:  redhat-lsb-core
BuildRequires:	Cython
BuildRequires:	python-prettytable
BuildRequires:	python-sphinx
%endif
# python34-... for RHEL, python3-... for all other supported distros
# no py3 in RH Ceph Storage
%if 0%{?rhel}
#BuildRequires:	python34-devel
#BuildRequires:	python34-setuptools
#BuildRequires:	python34-Cython
%else
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-Cython
%endif
# lttng and babeltrace for rbd-replay-prep
%if %{with lttng}
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	lttng-ust-devel
BuildRequires:	libbabeltrace-devel
%endif
%if 0%{?suse_version}
BuildRequires:	lttng-ust-devel
BuildRequires:  babeltrace-devel
%endif
%endif
%if 0%{?suse_version}
BuildRequires:	libexpat-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	expat-devel
%endif
#hardened-cc1
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:  redhat-rpm-config
%endif

%description
Ceph is a massively scalable, open-source, distributed storage system that runs
on commodity hardware and delivers object, block and file system storage.


#################################################################################
# subpackages
#################################################################################
%package base
Summary:       Ceph Base Package
%if 0%{?suse_version}
Group:         System/Filesystems
%endif
Requires:      ceph-common = %{_epoch_prefix}%{version}-%{release}
Requires:      librbd1 = %{_epoch_prefix}%{version}-%{release}
Requires:      librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:      libcephfs2 = %{_epoch_prefix}%{version}-%{release}
Requires:      librgw2 = %{_epoch_prefix}%{version}-%{release}
%if 0%{with selinux}
Requires:      ceph-selinux = %{_epoch_prefix}%{version}-%{release}
%endif
Requires:      python
Requires:      python-requests
Requires:      python-setuptools
Requires:      grep
Requires:      xfsprogs
Requires:      logrotate
Requires:      util-linux
Requires:      cryptsetup
Requires:      findutils
Requires:      psmisc
Requires:      which
%if 0%{?suse_version}
Recommends:    ntp-daemon
%endif
%description base
Base is the package that includes all the files shared amongst ceph servers

%package -n ceph-common
Summary:	Ceph Common
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:	libcephfs2 = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rados = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rbd = %{_epoch_prefix}%{version}-%{release}
Requires:	python-cephfs = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rgw = %{_epoch_prefix}%{version}-%{release}
%if 0%{?fedora} || 0%{?rhel}
Requires:	python-prettytable
%endif
%if 0%{?suse_version}
Requires:	python-PrettyTable
%endif
Requires:	python-requests
Requires:	gperftools-libs >= 2.4-8.el7
%{?systemd_requires}
%if 0%{?suse_version}
Requires(pre):	pwdutils
%endif
%description -n ceph-common
Common utilities to mount and interact with a ceph storage cluster.
Comprised of files that are common to Ceph clients and servers.

%package mds
Summary:	Ceph Metadata Server Daemon
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}-%{release}
%description mds
ceph-mds is the metadata server daemon for the Ceph distributed file system.
One or more instances of ceph-mds collectively manage the file system
namespace, coordinating access to the shared OSD cluster.

%package mon
Summary:	Ceph Monitor Daemon
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}-%{release}
# For ceph-rest-api
%if 0%{?fedora} || 0%{?rhel}
Requires:      python-flask
%endif
%if 0%{?suse_version}
Requires:      python-Flask
%endif
%description mon
ceph-mon is the cluster monitor daemon for the Ceph distributed file
system. One or more instances of ceph-mon form a Paxos part-time
parliament cluster that provides extremely reliable and durable storage
of cluster membership, configuration, and state.

%package mgr
Summary:        Ceph Manager Daemon
%if 0%{?suse_version}
Group:          System/Filesystems
%endif
Requires:       ceph-base = %{_epoch_prefix}%{version}-%{release}
%if 0%{?fedora} || 0%{?rhel}
Requires:       python-cherrypy
Requires:       python-jinja2
Requires:       python-werkzeug
Requires:       pyOpenSSL
%endif
%if 0%{?suse_version}
Requires: 	python-CherryPy
Requires:       python-Jinja2
Requires:       python-Werkzeug
Requires:       python-pyOpenSSL
%endif
Requires:       python-pecan
%description mgr
ceph-mgr enables python modules that provide services (such as the REST
module derived from Calamari) and expose CLI hooks.  ceph-mgr gathers
the cluster maps, the daemon metadata, and performance counters, and
exposes all these to the python modules.

%package fuse
Summary:	Ceph fuse-based client
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:       fuse
%description fuse
FUSE based client for Ceph distributed network file system

%package -n rbd-fuse
Summary:	Ceph fuse-based client
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
%description -n rbd-fuse
FUSE based client to map Ceph rbd images to files

%package -n rbd-mirror
Summary:	Ceph daemon for mirroring RBD images
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-common = %{_epoch_prefix}%{version}-%{release}
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
%description -n rbd-mirror
Daemon for mirroring RBD images between Ceph clusters, streaming
changes asynchronously.

%package -n rbd-nbd
Summary:	Ceph RBD client base on NBD
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
%description -n rbd-nbd
NBD based client to map Ceph rbd images to local device

%package radosgw
Summary:	Rados REST gateway
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-common = %{_epoch_prefix}%{version}-%{release}
%if 0%{with selinux}
Requires:	ceph-selinux = %{_epoch_prefix}%{version}-%{release}
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Requires:	librgw2 = %{_epoch_prefix}%{version}-%{release}
%if 0%{?rhel} || 0%{?fedora}
Requires:	mailcap
%endif
%description radosgw
RADOS is a distributed object store used by the Ceph distributed
storage system.  This package provides a REST gateway to the
object store that aims to implement a superset of Amazon's S3
service as well as the OpenStack Object Storage ("Swift") API.

%if %{with ocf}
%package resource-agents
Summary:	OCF-compliant resource agents for Ceph daemons
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}
Requires:	resource-agents
%description resource-agents
Resource agents for monitoring and managing Ceph daemons
under Open Cluster Framework (OCF) compliant resource
managers such as Pacemaker.
%endif

%package osd
Summary:	Ceph Object Storage Daemon
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}-%{release}
# for sgdisk, used by ceph-disk
%if 0%{?fedora} || 0%{?rhel}
Requires:	gdisk
%endif
%if 0%{?suse_version}
Requires:	gptfdisk
%endif
Requires:       parted >= 3.1-26
Requires:	lvm2
%description osd
ceph-osd is the object storage daemon for the Ceph distributed file
system.  It is responsible for storing objects on a local file system
and providing access to them over the network.

%package -n librados2
Summary:	RADOS distributed object store client library
%if 0%{?suse_version}
Group:		System/Libraries
%endif
%if 0%{?rhel} || 0%{?fedora}
Obsoletes:	ceph-libs < %{_epoch_prefix}%{version}-%{release}
%endif
%description -n librados2
RADOS is a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to access the distributed object
store using a simple file-like interface.

%package -n librados-devel
Summary:	RADOS headers
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	librados2-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	librados2-devel < %{_epoch_prefix}%{version}-%{release}
%description -n librados-devel
This package contains libraries and headers needed to develop programs
that use RADOS object store.

%package -n librgw2
Summary:	RADOS gateway client library
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
%description -n librgw2
This package provides a library implementation of the RADOS gateway
(distributed object store with S3 and Swift personalities).

%package -n librgw-devel
Summary:	RADOS gateway client library
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	librados-devel = %{_epoch_prefix}%{version}-%{release}
Requires:	librgw2 = %{_epoch_prefix}%{version}-%{release}
Provides:	librgw2-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	librgw2-devel < %{_epoch_prefix}%{version}-%{release}
%description -n librgw-devel
This package contains libraries and headers needed to develop programs
that use RADOS gateway client library.

%package -n python-rgw
Summary:	Python 2 libraries for the RADOS gateway
%if 0%{?suse_version}
Group:		Development/Languages/Python
%endif
Requires:	librgw2 = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rados = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	python-ceph < %{_epoch_prefix}%{version}-%{release}
%description -n python-rgw
This package contains Python 2 libraries for interacting with Cephs RADOS
gateway.

%package -n python-rados
Summary:	Python 2 libraries for the RADOS object store
%if 0%{?suse_version}
Group:		Development/Languages/Python
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	python-ceph < %{_epoch_prefix}%{version}-%{release}
%description -n python-rados
This package contains Python 2 libraries for interacting with Cephs RADOS
object store.

%package -n libradosstriper1
Summary:	RADOS striping interface
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
%description -n libradosstriper1
Striping interface built on top of the rados library, allowing
to stripe bigger objects onto several standard rados objects using
an interface very similar to the rados one.

%package -n libradosstriper-devel
Summary:	RADOS striping interface headers
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	libradosstriper1 = %{_epoch_prefix}%{version}-%{release}
Requires:	librados-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	libradosstriper1-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	libradosstriper1-devel < %{_epoch_prefix}%{version}-%{release}
%description -n libradosstriper-devel
This package contains libraries and headers needed to develop programs
that use RADOS striping interface.

%package -n librbd1
Summary:	RADOS block device client library
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	librados2 = %{_epoch_prefix}%{version}-%{release}
%if 0%{?suse_version}
Requires(post): coreutils
%endif
%if 0%{?rhel} || 0%{?fedora}
Obsoletes:	ceph-libs < %{_epoch_prefix}%{version}-%{release}
%endif
%description -n librbd1
RBD is a block device striped across multiple distributed objects in
RADOS, a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to manage these block devices.

%package -n librbd-devel
Summary:	RADOS block device headers
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
Requires:	librados-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	librbd1-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	librbd1-devel < %{_epoch_prefix}%{version}-%{release}
%description -n librbd-devel
This package contains libraries and headers needed to develop programs
that use RADOS block device.

%package -n python-rbd
Summary:	Python 2 libraries for the RADOS block device
%if 0%{?suse_version}
Group:		Development/Languages/Python
%endif
Requires:	librbd1 = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rados = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	python-ceph < %{_epoch_prefix}%{version}-%{release}
%description -n python-rbd
This package contains Python 2 libraries for interacting with Cephs RADOS
block device.

%package -n libcephfs2
Summary:	Ceph distributed file system client library
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Obsoletes:	libcephfs1
%if 0%{?rhel} || 0%{?fedora}
Obsoletes:	ceph-libs < %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-libcephfs
%endif
%description -n libcephfs2
Ceph is a distributed network file system designed to provide excellent
performance, reliability, and scalability. This is a shared library
allowing applications to access a Ceph distributed file system via a
POSIX-like interface.

%package -n libcephfs-devel
Summary:	Ceph distributed file system headers
%if 0%{?suse_version}
Group:		Development/Libraries/C and C++
%endif
Requires:	libcephfs2 = %{_epoch_prefix}%{version}-%{release}
Requires:	librados-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	libcephfs2-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	libcephfs2-devel < %{_epoch_prefix}%{version}-%{release}
%description -n libcephfs-devel
This package contains libraries and headers needed to develop programs
that use Cephs distributed file system.

%package -n python-cephfs
Summary:	Python 2 libraries for Ceph distributed file system
%if 0%{?suse_version}
Group:		Development/Languages/Python
%endif
Requires:	libcephfs2 = %{_epoch_prefix}%{version}-%{release}
%if 0%{?suse_version}
Recommends: python-rados = %{_epoch_prefix}%{version}-%{release}
%endif
Obsoletes:	python-ceph < %{_epoch_prefix}%{version}-%{release}
%description -n python-cephfs
This package contains Python 2 libraries for interacting with Cephs distributed
file system.

%if 0%{with ceph_test_package}
%package -n ceph-test
Summary:	Ceph benchmarks and test tools
%if 0%{?suse_version}
Group:		System/Benchmark
%endif
Requires:	ceph-common = %{_epoch_prefix}%{version}-%{release}
Requires:	xmlstarlet
Requires:	jq
Requires:	socat
%description -n ceph-test
This package contains Ceph benchmarks and test tools.
%endif

%if 0%{with cephfs_java}

%package -n libcephfs_jni1
Summary:	Java Native Interface library for CephFS Java bindings
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	java
Requires:	libcephfs2 = %{_epoch_prefix}%{version}-%{release}
%description -n libcephfs_jni1
This package contains the Java Native Interface library for CephFS Java
bindings.

%package -n libcephfs_jni-devel
Summary:	Development files for CephFS Java Native Interface library
%if 0%{?suse_version}
Group:		Development/Libraries/Java
%endif
Requires:	java
Requires:	libcephfs_jni1 = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	ceph-devel < %{_epoch_prefix}%{version}-%{release}
Provides:	libcephfs_jni1-devel = %{_epoch_prefix}%{version}-%{release}
Obsoletes:	libcephfs_jni1-devel < %{_epoch_prefix}%{version}-%{release}
%description -n libcephfs_jni-devel
This package contains the development files for CephFS Java Native Interface
library.

%package -n cephfs-java
Summary:	Java libraries for the Ceph File System
%if 0%{?suse_version}
Group:		System/Libraries
%endif
Requires:	java
Requires:	libcephfs_jni1 = %{_epoch_prefix}%{version}-%{release}
Requires:       junit
BuildRequires:  junit
%description -n cephfs-java
This package contains the Java libraries for the Ceph File System.

%endif

%package -n rados-objclass-devel
Summary:        RADOS object class development kit
Group:          Development/Libraries
Requires:       librados2-devel = %{_epoch_prefix}%{version}-%{release}
%description -n rados-objclass-devel
This package contains libraries and headers needed to develop RADOS object
class plugins.

%if 0%{with selinux}

%package selinux
Summary:	SELinux support for Ceph MON, OSD and MDS
%if 0%{?suse_version}
Group:		System/Filesystems
%endif
Requires:	ceph-base = %{_epoch_prefix}%{version}-%{release}
Requires:	policycoreutils, libselinux-utils
Requires(post):	ceph-base = %{_epoch_prefix}%{version}-%{release}
Requires(post): selinux-policy-base >= %{_selinux_policy_version}, policycoreutils, gawk
Requires(postun): policycoreutils
%description selinux
This package contains SELinux support for Ceph MON, OSD and MDS. The package
also performs file-system relabelling which can take a long time on heavily
populated file-systems.

%endif

%package -n python-ceph-compat
Summary:	Compatibility package for Cephs python libraries
%if 0%{?suse_version}
Group:		Development/Languages/Python
%endif
Obsoletes:	python-ceph
Requires:	python-rados = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rbd = %{_epoch_prefix}%{version}-%{release}
Requires:	python-cephfs = %{_epoch_prefix}%{version}-%{release}
Requires:	python-rgw = %{_epoch_prefix}%{version}-%{release}
Provides:	python-ceph
%description -n python-ceph-compat
This is a compatibility package to accommodate python-ceph split into
python-rados, python-rbd, python-rgw and python-cephfs. Packages still
depending on python-ceph should be fixed to depend on python-rados,
python-rbd, python-rgw or python-cephfs instead.

#################################################################################
# common
#################################################################################
%prep
%autosetup -p1

# Rewrite .git_version file.
# `rdopkg update-patches` will automatically update this macro:
%global commit d4b9f17b56b3348566926849313084dd6efc2ca2
# and then the macro gets written into .git_version:
echo %{commit} > src/.git_version
echo v%{version}-%{release} >> src/.git_version

%build
%if 0%{with cephfs_java}
# Find jni.h
for i in /usr/{lib64,lib}/jvm/java/include{,/linux}; do
    [ -d $i ] && java_inc="$java_inc -I$i"
done
%endif

%if %{with lowmem_builder}
RPM_OPT_FLAGS="$RPM_OPT_FLAGS --param ggc-min-expand=20 --param ggc-min-heapsize=32768"
%endif
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/i386/i486/'`

export CPPFLAGS="$java_inc"
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

env | sort

%if %{with lowmem_builder}
%if 0%{?jobs} > 8
%define _smp_mflags -j8
%endif
%endif

# unlimit _smp_mflags in system macro if not set above
# Brew cannot handle -j24 here
%define _smp_ncpus_max 16
# extract the number of processors for use with cmake
%define _smp_ncpus %(echo %{_smp_mflags} | sed 's/-j//')

mkdir build
cd build
cmake .. \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_LIBEXECDIR=%{_libexecdir} \
    -DCMAKE_INSTALL_LOCALSTATEDIR=%{_localstatedir} \
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DCMAKE_INSTALL_MANDIR=%{_mandir} \
    -DCMAKE_INSTALL_DOCDIR=%{_docdir}/ceph \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DWITH_EMBEDDED=OFF \
    -DWITH_MANPAGE=ON \
    -DWITH_PYTHON3=OFF \
    -DWITH_SYSTEMD=ON \
%if 0%{?rhel} && ! 0%{?centos}
    -DWITH_SUBMAN=ON \
%endif
%if 0%{without ceph_test_package}
    -DWITH_TESTS=OFF \
%endif
%if 0%{with cephfs_java}
    -DWITH_CEPHFS_JAVA=ON \
%endif
%if 0%{with selinux}
    -DWITH_SELINUX=ON \
%endif
%if %{with lttng}
    -DWITH_LTTNG=ON \
    -DWITH_BABELTRACE=ON \
%else
    -DWITH_LTTNG=OFF \
    -DWITH_BABELTRACE=OFF \
%endif
    $CEPH_EXTRA_CMAKE_ARGS \
%if 0%{with ocf}
    -DWITH_OCF=ON \
%endif
%ifarch aarch64 armv7hl mips mipsel ppc ppc64 ppc64le %{ix86} x86_64
    -DWITH_BOOST_CONTEXT=ON \
%else
    -DWITH_BOOST_CONTEXT=OFF \
%endif
    -DBOOST_J=%{_smp_ncpus}

make %{?_smp_mflags}


%if 0%{with make_check}
%check
# run in-tree unittests
cd build
ctest %{?_smp_mflags}

%endif



%install
pushd build
make DESTDIR=%{buildroot} install
# we have dropped sysvinit bits
rm -f %{buildroot}/%{_sysconfdir}/init.d/ceph
popd
install -m 0644 -D src/etc-rbdmap %{buildroot}%{_sysconfdir}/ceph/rbdmap
%if 0%{?fedora} || 0%{?rhel}
install -m 0644 -D etc/sysconfig/ceph %{buildroot}%{_sysconfdir}/sysconfig/ceph
%endif
%if 0%{?suse_version}
install -m 0644 -D etc/sysconfig/ceph %{buildroot}%{_localstatedir}/adm/fillup-templates/sysconfig.%{name}
%endif
install -m 0644 -D systemd/ceph.tmpfiles.d %{buildroot}%{_tmpfilesdir}/ceph-common.conf
install -m 0755 -D systemd/ceph %{buildroot}%{_sbindir}/rcceph
install -m 0644 -D systemd/50-ceph.preset %{buildroot}%{_libexecdir}/systemd/system-preset/50-ceph.preset
mkdir -p %{buildroot}%{_sbindir}
install -m 0644 -D src/logrotate.conf %{buildroot}%{_sysconfdir}/logrotate.d/ceph
chmod 0644 %{buildroot}%{_docdir}/ceph/sample.ceph.conf
install -m 0644 -D COPYING %{buildroot}%{_docdir}/ceph/COPYING
install -m 0644 -D etc/sysctl/90-ceph-osd.conf %{buildroot}%{_sysctldir}/90-ceph-osd.conf

# firewall templates and /sbin/mount.ceph symlink
%if 0%{?suse_version}
install -m 0644 -D etc/sysconfig/SuSEfirewall2.d/services/ceph-mon %{buildroot}%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/ceph-mon
install -m 0644 -D etc/sysconfig/SuSEfirewall2.d/services/ceph-osd-mds %{buildroot}%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/ceph-osd-mds
mkdir -p %{buildroot}/sbin
ln -sf %{_sbindir}/mount.ceph %{buildroot}/sbin/mount.ceph
%endif

# udev rules
install -m 0644 -D udev/50-rbd.rules %{buildroot}%{_udevrulesdir}/50-rbd.rules
install -m 0644 -D udev/60-ceph-by-parttypeuuid.rules %{buildroot}%{_udevrulesdir}/60-ceph-by-parttypeuuid.rules
install -m 0644 -D udev/95-ceph-osd.rules %{buildroot}%{_udevrulesdir}/95-ceph-osd.rules

#set up placeholder directories
mkdir -p %{buildroot}%{_sysconfdir}/ceph
mkdir -p %{buildroot}%{_localstatedir}/run/ceph
mkdir -p %{buildroot}%{_localstatedir}/log/ceph
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/tmp
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mon
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/osd
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mds
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/mgr
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/radosgw
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-osd
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-mds
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-rgw
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-mgr
mkdir -p %{buildroot}%{_localstatedir}/lib/ceph/bootstrap-rbd

%if 0%{?suse_version}
# create __pycache__ directories and their contents
%py3_compile %{buildroot}%{python3_sitelib}
%endif

%clean
rm -rf %{buildroot}

#################################################################################
# files and systemd scriptlets
#################################################################################
%files

%files base
%{_bindir}/crushtool
%{_bindir}/monmaptool
%{_bindir}/osdmaptool
%{_bindir}/ceph-kvstore-tool
%{_bindir}/ceph-run
%{_bindir}/ceph-detect-init
%{_libexecdir}/systemd/system-preset/50-ceph.preset
%{_sbindir}/ceph-create-keys
%{_sbindir}/ceph-disk
%{_sbindir}/rcceph
%dir %{_libexecdir}/ceph
%{_libexecdir}/ceph/ceph_common.sh
%dir %{_libdir}/rados-classes
%{_libdir}/rados-classes/*
%dir %{_libdir}/ceph
%dir %{_libdir}/ceph/erasure-code
%{_libdir}/ceph/erasure-code/libec_*.so*
%dir %{_libdir}/ceph/compressor
%{_libdir}/ceph/compressor/libceph_*.so*
%ifarch x86_64
%dir %{_libdir}/ceph/crypto
%{_libdir}/ceph/crypto/libceph_*.so*
%endif
%if %{with lttng}
%{_libdir}/libos_tp.so*
%{_libdir}/libosd_tp.so*
%endif
%config(noreplace) %{_sysconfdir}/logrotate.d/ceph
%if 0%{?fedora} || 0%{?rhel}
%config(noreplace) %{_sysconfdir}/sysconfig/ceph
%endif
%if 0%{?suse_version}
%{_localstatedir}/adm/fillup-templates/sysconfig.*
%config %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/ceph-mon
%config %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/ceph-osd-mds
%endif
%{_unitdir}/ceph-disk@.service
%{_unitdir}/ceph.target
%{python_sitelib}/ceph_detect_init*
%{python_sitelib}/ceph_disk*
%dir %{python_sitelib}/ceph_volume
%{python_sitelib}/ceph_volume/*
%{python_sitelib}/ceph_volume-*
%{_mandir}/man8/ceph-deploy.8*
%{_mandir}/man8/ceph-detect-init.8*
%{_mandir}/man8/ceph-create-keys.8*
%{_mandir}/man8/ceph-disk.8*
%{_mandir}/man8/ceph-run.8*
%{_mandir}/man8/crushtool.8*
%{_mandir}/man8/osdmaptool.8*
%{_mandir}/man8/monmaptool.8*
%{_mandir}/man8/ceph-kvstore-tool.8*
#set up placeholder directories
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/tmp
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-osd
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-mds
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-rgw
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-mgr
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/bootstrap-rbd

%post base
/sbin/ldconfig
%if 0%{?suse_version}
%fillup_only
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl preset ceph-disk@\*.service ceph.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-disk@\*.service ceph.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph.target >/dev/null 2>&1 || :
fi

%preun base
%if 0%{?suse_version}
%service_del_preun ceph-disk@\*.service ceph.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-disk@\*.service ceph.target
%endif

%postun base
/sbin/ldconfig
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-disk@\*.service ceph.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-disk@\*.service ceph.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-disk@\*.service > /dev/null 2>&1 || :
  fi
fi

%files common
%dir %{_docdir}/ceph
%doc %{_docdir}/ceph/sample.ceph.conf
%doc %{_docdir}/ceph/COPYING
%{_bindir}/ceph
%{_bindir}/ceph-authtool
%{_bindir}/ceph-conf
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-rbdnamer
%{_bindir}/ceph-syn
%{_bindir}/ceph-crush-location
%{_bindir}/cephfs-data-scan
%{_bindir}/cephfs-journal-tool
%{_bindir}/cephfs-table-tool
%{_bindir}/rados
%{_bindir}/radosgw-admin
%{_bindir}/rbd
%{_bindir}/rbd-replay
%{_bindir}/rbd-replay-many
%{_bindir}/rbdmap
%{_sbindir}/mount.ceph
%if 0%{?suse_version}
/sbin/mount.ceph
%endif
%if %{with lttng}
%{_bindir}/rbd-replay-prep
%endif
%{_bindir}/ceph-post-file
%{_bindir}/ceph-brag
%{_tmpfilesdir}/ceph-common.conf
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph-dencoder.8*
%{_mandir}/man8/ceph-rbdnamer.8*
%{_mandir}/man8/ceph-syn.8*
%{_mandir}/man8/ceph-post-file.8*
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/mount.ceph.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/radosgw-admin.8*
%{_mandir}/man8/rbd.8*
%{_mandir}/man8/rbdmap.8*
%{_mandir}/man8/rbd-replay.8*
%{_mandir}/man8/rbd-replay-many.8*
%{_mandir}/man8/rbd-replay-prep.8*
%dir %{_datadir}/ceph/
%{_datadir}/ceph/known_hosts_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com
%{_datadir}/ceph/id_rsa_drop.ceph.com.pub
%dir %{_sysconfdir}/ceph/
%config %{_sysconfdir}/bash_completion.d/ceph
%config %{_sysconfdir}/bash_completion.d/rados
%config %{_sysconfdir}/bash_completion.d/rbd
%config %{_sysconfdir}/bash_completion.d/radosgw-admin
%config(noreplace) %{_sysconfdir}/ceph/rbdmap
%{_unitdir}/rbdmap.service
%{python_sitelib}/ceph_argparse.py*
%{python_sitelib}/ceph_daemon.py*
%dir %{_udevrulesdir}
%{_udevrulesdir}/50-rbd.rules
%attr(3770,ceph,ceph) %dir %{_localstatedir}/log/ceph/
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/

%pre common
CEPH_GROUP_ID=167
CEPH_USER_ID=167
%if 0%{?rhel} || 0%{?fedora}
/usr/sbin/groupadd ceph -g $CEPH_GROUP_ID -o -r 2>/dev/null || :
/usr/sbin/useradd ceph -u $CEPH_USER_ID -o -r -g ceph -s /sbin/nologin -c "Ceph daemons" -d %{_localstatedir}/lib/ceph 2>/dev/null || :
%endif
%if 0%{?suse_version}
if ! getent group ceph >/dev/null ; then
    CEPH_GROUP_ID_OPTION=""
    getent group $CEPH_GROUP_ID >/dev/null || CEPH_GROUP_ID_OPTION="-g $CEPH_GROUP_ID"
    groupadd ceph $CEPH_GROUP_ID_OPTION -r 2>/dev/null || :
fi
if ! getent passwd ceph >/dev/null ; then
    CEPH_USER_ID_OPTION=""
    getent passwd $CEPH_USER_ID >/dev/null || CEPH_USER_ID_OPTION="-u $CEPH_USER_ID"
    useradd ceph $CEPH_USER_ID_OPTION -r -g ceph -s /sbin/nologin 2>/dev/null || :
fi
usermod -c "Ceph storage service" \
        -d %{_localstatedir}/lib/ceph \
        -g ceph \
        -s /sbin/nologin \
        ceph
%endif
exit 0

%post common
%tmpfiles_create %{_tmpfilesdir}/ceph-common.conf

%postun common
# Package removal cleanup
if [ "$1" -eq "0" ] ; then
    rm -rf %{_localstatedir}/log/ceph
    rm -rf %{_sysconfdir}/ceph
fi

%files mds
%{_bindir}/ceph-mds
%{_mandir}/man8/ceph-mds.8*
%{_unitdir}/ceph-mds@.service
%{_unitdir}/ceph-mds.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mds

%post mds
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-mds@\*.service ceph-mds.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-mds@\*.service ceph-mds.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-mds.target >/dev/null 2>&1 || :
fi

%preun mds
%if 0%{?suse_version}
%service_del_preun ceph-mds@\*.service ceph-mds.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-mds@\*.service ceph-mds.target
%endif

%postun mds
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-mds@\*.service ceph-mds.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-mds@\*.service ceph-mds.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mds@\*.service > /dev/null 2>&1 || :
  fi
fi

%files mgr
%{_bindir}/ceph-mgr
%{_libdir}/ceph/mgr
%{_unitdir}/ceph-mgr@.service
%{_unitdir}/ceph-mgr.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mgr

%post mgr
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-mgr@\*.service ceph-mgr.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-mgr@\*.service ceph-mgr.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-mgr.target >/dev/null 2>&1 || :
fi

%preun mgr
%if 0%{?suse_version}
%service_del_preun ceph-mgr@\*.service ceph-mgr.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-mgr@\*.service ceph-mgr.target
%endif

%postun mgr
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-mgr@\*.service ceph-mgr.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-mgr@\*.service ceph-mgr.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mgr@\*.service > /dev/null 2>&1 || :
  fi
fi

%files mon
%{_bindir}/ceph-mon
%{_bindir}/ceph-rest-api
%{_bindir}/ceph-monstore-tool
%{_mandir}/man8/ceph-mon.8*
%{_mandir}/man8/ceph-rest-api.8*
%{python_sitelib}/ceph_rest_api.py*
%{_unitdir}/ceph-mon@.service
%{_unitdir}/ceph-mon.target
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/mon

%post mon
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-mon@\*.service ceph-mon.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-mon@\*.service ceph-mon.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-mon.target >/dev/null 2>&1 || :
fi

%preun mon
%if 0%{?suse_version}
%service_del_preun ceph-mon@\*.service ceph-mon.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-mon@\*.service ceph-mon.target
%endif

%postun mon
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-mon@\*.service ceph-mon.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-mon@\*.service ceph-mon.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-mon@\*.service > /dev/null 2>&1 || :
  fi
fi

%files fuse
%{_bindir}/ceph-fuse
%{_mandir}/man8/ceph-fuse.8*
%{_sbindir}/mount.fuse.ceph
%{_unitdir}/ceph-fuse@.service
%{_unitdir}/ceph-fuse.target

%files -n rbd-fuse
%{_bindir}/rbd-fuse
%{_mandir}/man8/rbd-fuse.8*

%files -n rbd-mirror
%{_bindir}/rbd-mirror
%{_mandir}/man8/rbd-mirror.8*
%{_unitdir}/ceph-rbd-mirror@.service
%{_unitdir}/ceph-rbd-mirror.target

%post -n rbd-mirror
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-rbd-mirror@\*.service ceph-rbd-mirror.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-rbd-mirror.target >/dev/null 2>&1 || :
fi

%preun -n rbd-mirror
%if 0%{?suse_version}
%service_del_preun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif

%postun -n rbd-mirror
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-rbd-mirror@\*.service ceph-rbd-mirror.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-rbd-mirror@\*.service > /dev/null 2>&1 || :
  fi
fi

%files -n rbd-nbd
%{_bindir}/rbd-nbd
%{_mandir}/man8/rbd-nbd.8*

%files radosgw
%{_bindir}/radosgw
%{_bindir}/radosgw-token
%{_bindir}/radosgw-es
%{_bindir}/radosgw-object-expirer
%{_mandir}/man8/radosgw.8*
%dir %{_localstatedir}/lib/ceph/radosgw
%{_unitdir}/ceph-radosgw@.service
%{_unitdir}/ceph-radosgw.target

%post radosgw
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-radosgw@\*.service ceph-radosgw.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-radosgw@\*.service ceph-radosgw.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-radosgw.target >/dev/null 2>&1 || :
fi

%preun radosgw
%if 0%{?suse_version}
%service_del_preun ceph-radosgw@\*.service ceph-radosgw.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-radosgw@\*.service ceph-radosgw.target
%endif

%postun radosgw
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-radosgw@\*.service ceph-radosgw.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-radosgw@\*.service ceph-radosgw.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-radosgw@\*.service > /dev/null 2>&1 || :
  fi
fi

%files osd
%{_bindir}/ceph-clsinfo
%{_bindir}/ceph-bluestore-tool
%{_bindir}/ceph-objectstore-tool
%{_bindir}/ceph-osdomap-tool
%{_bindir}/ceph-osd
%{_libexecdir}/ceph/ceph-osd-prestart.sh
%{_sbindir}/ceph-volume
%{_sbindir}/ceph-volume-systemd
%dir %{_udevrulesdir}
%{_udevrulesdir}/60-ceph-by-parttypeuuid.rules
%{_udevrulesdir}/95-ceph-osd.rules
%{_mandir}/man8/ceph-clsinfo.8*
%{_mandir}/man8/ceph-osd.8*
%{_mandir}/man8/ceph-bluestore-tool.8*
%{_mandir}/man8/ceph-volume.8*
%{_mandir}/man8/ceph-volume-systemd.8*
%if 0%{?rhel} && ! 0%{?centos}
%attr(0755,-,-) %{_sysconfdir}/cron.hourly/subman
%endif
%{_unitdir}/ceph-osd@.service
%{_unitdir}/ceph-osd.target
%{_unitdir}/ceph-volume@.service
%attr(750,ceph,ceph) %dir %{_localstatedir}/lib/ceph/osd
%config(noreplace) %{_sysctldir}/90-ceph-osd.conf

%post osd
%if 0%{?suse_version}
if [ $1 -eq 1 ] ; then
  /usr/bin/systemctl preset ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target >/dev/null 2>&1 || :
fi
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_post ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif
if [ $1 -eq 1 ] ; then
/usr/bin/systemctl start ceph-osd.target >/dev/null 2>&1 || :
fi
%if 0%{?sysctl_apply}
    %sysctl_apply 90-ceph-osd.conf
%else
    /usr/lib/systemd/systemd-sysctl %{_sysctldir}/90-ceph-osd.conf > /dev/null 2>&1 || :
%endif

%preun osd
%if 0%{?suse_version}
%service_del_preun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_preun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif

%postun osd
test -n "$FIRST_ARG" || FIRST_ARG=$1
%if 0%{?suse_version}
DISABLE_RESTART_ON_UPDATE="yes"
%service_del_postun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif
%if 0%{?fedora} || 0%{?rhel}
%systemd_postun ceph-osd@\*.service ceph-volume@\*.service ceph-osd.target
%endif
if [ $FIRST_ARG -ge 1 ] ; then
  # Restart on upgrade, but only if "CEPH_AUTO_RESTART_ON_UPGRADE" is set to
  # "yes". In any case: if units are not running, do not touch them.
  SYSCONF_CEPH=%{_sysconfdir}/sysconfig/ceph
  if [ -f $SYSCONF_CEPH -a -r $SYSCONF_CEPH ] ; then
    source $SYSCONF_CEPH
  fi
  if [ "X$CEPH_AUTO_RESTART_ON_UPGRADE" = "Xyes" ] ; then
    /usr/bin/systemctl try-restart ceph-osd@\*.service ceph-volume@\*.service > /dev/null 2>&1 || :
  fi
fi

%if %{with ocf}

%files resource-agents
%dir %{_prefix}/lib/ocf
%dir %{_prefix}/lib/ocf/resource.d
%dir %{_prefix}/lib/ocf/resource.d/ceph
%attr(0755,-,-) %{_prefix}/lib/ocf/resource.d/ceph/rbd

%endif

%files -n librados2
%{_libdir}/librados.so.*
%dir %{_libdir}/ceph
%{_libdir}/ceph/libceph-common.so*
%if %{with lttng}
%{_libdir}/librados_tp.so.*
%endif

%post -n librados2 -p /sbin/ldconfig

%postun -n librados2 -p /sbin/ldconfig

%files -n librados-devel
%dir %{_includedir}/rados
%{_includedir}/rados/librados.h
%{_includedir}/rados/librados.hpp
%{_includedir}/rados/buffer.h
%{_includedir}/rados/buffer_fwd.h
%{_includedir}/rados/inline_memory.h
%{_includedir}/rados/page.h
%{_includedir}/rados/crc32c.h
%{_includedir}/rados/rados_types.h
%{_includedir}/rados/rados_types.hpp
%{_includedir}/rados/memory.h
%{_libdir}/librados.so
%if %{with lttng}
%{_libdir}/librados_tp.so
%endif
%{_bindir}/librados-config
%{_mandir}/man8/librados-config.8*

%files -n python-rados
%{python_sitearch}/rados.so
%{python_sitearch}/rados-*.egg-info

%files -n libradosstriper1
%{_libdir}/libradosstriper.so.*

%post -n libradosstriper1 -p /sbin/ldconfig

%postun -n libradosstriper1 -p /sbin/ldconfig

%files -n libradosstriper-devel
%dir %{_includedir}/radosstriper
%{_includedir}/radosstriper/libradosstriper.h
%{_includedir}/radosstriper/libradosstriper.hpp
%{_libdir}/libradosstriper.so

%files -n librbd1
%{_libdir}/librbd.so.*
%if %{with lttng}
%{_libdir}/librbd_tp.so.*
%endif

%post -n librbd1 -p /sbin/ldconfig

%postun -n librbd1 -p /sbin/ldconfig

%files -n librbd-devel
%dir %{_includedir}/rbd
%{_includedir}/rbd/librbd.h
%{_includedir}/rbd/librbd.hpp
%{_includedir}/rbd/features.h
%{_libdir}/librbd.so
%if %{with lttng}
%{_libdir}/librbd_tp.so
%endif

%files -n librgw2
%{_libdir}/librgw.so.*

%post -n librgw2 -p /sbin/ldconfig

%postun -n librgw2 -p /sbin/ldconfig

%files -n librgw-devel
%dir %{_includedir}/rados
%{_includedir}/rados/librgw.h
%{_includedir}/rados/rgw_file.h
%{_libdir}/librgw.so

%files -n python-rgw
%{python_sitearch}/rgw.so
%{python_sitearch}/rgw-*.egg-info

%files -n python-rbd
%{python_sitearch}/rbd.so
%{python_sitearch}/rbd-*.egg-info

%files -n libcephfs2
%{_libdir}/libcephfs.so.*

%post -n libcephfs2 -p /sbin/ldconfig

%postun -n libcephfs2 -p /sbin/ldconfig

%files -n libcephfs-devel
%dir %{_includedir}/cephfs
%{_includedir}/cephfs/libcephfs.h
%{_includedir}/cephfs/ceph_statx.h
%{_libdir}/libcephfs.so

%files -n python-cephfs
%{python_sitearch}/cephfs.so
%{python_sitearch}/cephfs-*.egg-info
%{python_sitelib}/ceph_volume_client.py*

%if 0%{with ceph_test_package}
%files -n ceph-test
%{_bindir}/ceph-client-debug
%{_bindir}/ceph_bench_log
%{_bindir}/ceph_kvstorebench
%{_bindir}/ceph_multi_stress_watch
%{_bindir}/ceph_erasure_code
%{_bindir}/ceph_erasure_code_benchmark
%{_bindir}/ceph_omapbench
%{_bindir}/ceph_objectstore_bench
%{_bindir}/ceph_perf_objectstore
%{_bindir}/ceph_perf_local
%{_bindir}/ceph_perf_msgr_client
%{_bindir}/ceph_perf_msgr_server
%{_bindir}/ceph_psim
%{_bindir}/ceph_radosacl
%{_bindir}/ceph_rgw_jsonparser
%{_bindir}/ceph_rgw_multiparser
%{_bindir}/ceph_scratchtool
%{_bindir}/ceph_scratchtoolpp
%{_bindir}/ceph_smalliobench
%{_bindir}/ceph_smalliobenchdumb
%{_bindir}/ceph_smalliobenchfs
%{_bindir}/ceph_smalliobenchrbd
%{_bindir}/ceph_test_*
%{_bindir}/ceph_tpbench
%{_bindir}/ceph_xattr_bench
%{_bindir}/ceph-coverage
%{_bindir}/ceph-debugpack
%{_mandir}/man8/ceph-debugpack.8*
%dir %{_libdir}/ceph
%{_libdir}/ceph/ceph-monstore-update-crush.sh
%endif

%if 0%{with cephfs_java}
%files -n libcephfs_jni1
%{_libdir}/libcephfs_jni.so.*

%post -n libcephfs_jni1 -p /sbin/ldconfig

%postun -n libcephfs_jni1 -p /sbin/ldconfig

%files -n libcephfs_jni-devel
%{_libdir}/libcephfs_jni.so

%files -n cephfs-java
%{_javadir}/libcephfs.jar
%{_javadir}/libcephfs-test.jar
%endif

%files -n rados-objclass-devel
%dir %{_includedir}/rados
%{_includedir}/rados/objclass.h

%if 0%{with selinux}
%files selinux
%attr(0600,root,root) %{_datadir}/selinux/packages/ceph.pp
%{_datadir}/selinux/devel/include/contrib/ceph.if
%{_mandir}/man8/ceph_selinux.8*

%post selinux
# backup file_contexts before update
. /etc/selinux/config
FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

# Install the policy
/usr/sbin/semodule -i %{_datadir}/selinux/packages/ceph.pp

# Load the policy if SELinux is enabled
if ! /usr/sbin/selinuxenabled; then
    # Do not relabel if selinux is not enabled
    exit 0
fi

if diff ${FILE_CONTEXT} ${FILE_CONTEXT}.pre > /dev/null 2>&1; then
   # Do not relabel if file contexts did not change
   exit 0
fi

# Check whether the daemons are running
/usr/bin/systemctl status ceph.target > /dev/null 2>&1
STATUS=$?

# Stop the daemons if they were running
if test $STATUS -eq 0; then
    /usr/bin/systemctl stop ceph.target > /dev/null 2>&1
fi

# Relabel the files
# Use ceph-disk fix for first package install and fixfiles otherwise
if [ "$1" = "1" ]; then
    /usr/sbin/ceph-disk fix --selinux
else
    /usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null
fi

rm -f ${FILE_CONTEXT}.pre
# The fixfiles command won't fix label for /var/run/ceph
/usr/sbin/restorecon -R /var/run/ceph > /dev/null 2>&1

# Start the daemons iff they were running before
if test $STATUS -eq 0; then
    /usr/bin/systemctl start ceph.target > /dev/null 2>&1 || :
fi
exit 0

%postun selinux
if [ $1 -eq 0 ]; then
    # backup file_contexts before update
    . /etc/selinux/config
    FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
    cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

    # Remove the module
    /usr/sbin/semodule -n -r ceph > /dev/null 2>&1

    # Reload the policy if SELinux is enabled
    if ! /usr/sbin/selinuxenabled ; then
        # Do not relabel if SELinux is not enabled
        exit 0
    fi

    # Check whether the daemons are running
    /usr/bin/systemctl status ceph.target > /dev/null 2>&1
    STATUS=$?

    # Stop the daemons if they were running
    if test $STATUS -eq 0; then
        /usr/bin/systemctl stop ceph.target > /dev/null 2>&1
    fi

    /usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null
    rm -f ${FILE_CONTEXT}.pre
    # The fixfiles command won't fix label for /var/run/ceph
    /usr/sbin/restorecon -R /var/run/ceph > /dev/null 2>&1

    # Start the daemons if they were running before
    if test $STATUS -eq 0; then
	/usr/bin/systemctl start ceph.target > /dev/null 2>&1 || :
    fi
fi
exit 0

%endif # with selinux

%files -n python-ceph-compat
# We need an empty %%files list for python-ceph-compat, to tell rpmbuild to
# actually build this meta package.


%changelog
* Fri Oct 12 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-59
- luminous: filestore: add pgid in filestore pg dir split log message (rhbz#1599005)

* Thu Oct 11 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-58
- rgw: RemoteApplier::create_account() applies default quota config (rhbz#1630870)
- rgw: add helper functions to apply configured default quotas (rhbz#1630870)
- rgw: remove redundant quota logic from admin/user api (rhbz#1630870)

* Mon Oct 08 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-57
- mds: use monotonic waits in Beacon (rhbz#1628307)
- mds: use monotonic clock in beacon (rhbz#1628307)
- mds: simplify beacon init (rhbz#1628307)

* Fri Oct 05 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-56
- rgw: copy actual stats from the source shards during reshard (rhbz#1636562)

* Thu Oct 04 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-55
- osd/OSDMap: CRUSH_TUNABLES5 added in jewel, not kraken (rhbz#1636253)
- crush/CrushWrapper: clean up member init (rhbz#1636253)
- messages/MOSDMap: significant feature bits. (rhbz#1636253)
- mon/OSDMonitor: add feature into osdmap cache key. (rhbz#1636253)
- mon/OSDMonitor: move OSDMap feature calculation into OSDMap helper (rhbz#1636253)
- osd/OSDMap: add SIGNIFICANT_FEATURES and helper (rhbz#1636253)
- mon/HealthMonitor: do not send MMonHealthChecks to pre-luminous mon (rhbz#1636243)

* Wed Oct 03 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-54
- rgw: bucket link: "bucket move" documentation changes (rhbz#1595379)
- rgw: bucket link: "bucket move"; handle bucket names too. (rhbz#1595379)
- rgw: bucket link: base "bucket move" (tenant id only) (rhbz#1595379)
- rearrange / simplify RGWBucket::link logic - start bucket move support (rhbz#1595379)
- rgw: bucket link: use data from bucket_info to rewrite bucket_endpoint. (rhbz#1595379)
- rgw: bucket link: simplify use of get bucket info. (rhbz#1595379)
- rgw: bucket link: Add ability to name bucket w/ different tenant. (rhbz#1595379)
- Add "--bucket-new-name" option to radosgw-admin. (rhbz#1595379)
- Add several types to ceph-dencoder. (rhbz#1595379)
- rgw: RGWBucket::link supports tenant (rhbz#1595379)
- rgw: making implicit_tenants backwards compatible. (rhbz#1595379)

* Wed Oct 03 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-53
- rgw: enable override of tcmalloc linkage (rhbz#1635805)

* Wed Oct 03 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-52
- rgw: fix chunked-encoding for chunks >1MiB (rhbz#1635259)

* Tue Oct 02 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-51
- *: set missing CLOEXEC on opened fds (rhbz#1627553)
- msg: set O_NONBLOCK on file status flags (rhbz#1627553)

* Tue Oct 02 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-50
- rgw: abort_bucket_multiparts() ignores individual NoSuchUpload errors (rhbz#1628055)
- rgw: optimize function abort_bucket_multiparts (rhbz#1628055)
- rgw: raise debug level on redundant data sync error messages (rhbz#1626239)

* Tue Oct 02 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-49
- client: retry remount on dcache invalidation failure (rhbz#1614780)

* Mon Oct 01 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-48
- qa/standalone/osd/ec-error-rollforward: reproduce bug 24597 (rhbz#1634786)
- qa/standalone/osd/repro_long_log.sh: fix test (rhbz#1634786)
- osd/PG: do not blindly roll forward to log.head (rhbz#1634786)

* Fri Sep 28 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-47
- librbd: utilize the journal disabled policy when removing images (rhbz#1561758)
- librbd: fix refuse to release lock when cookie is the same at rewatch (rhbz#1622697)
- mds: cleanup MDSRank::evict_client (rhbz#1623264)
- mds: improve error handling in PurgeQueue (rhbz#1607581)
- mds: health warning for slow metadata IO (rhbz#1607590)
- mds: avoid using g_conf->get_val<...>(...) in hot path (rhbz#1607595)
- ceph_volume_client: add delay for MDSMap to be distributed (rhbz#1612378)
- client: check for unmounted condition before printing debug output (rhbz#1615394)
- mds: more description for failed authpin (rhbz#1628312)
- mds: cleanup CDir freezing/frozen tree check (rhbz#1628312)

* Wed Sep 26 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-46
- mds: don't modify filepath when printing (rhbz#1628314)
- mds: hold slave request refernce when dumping MDRequestImpl (rhbz#1628314)

* Wed Sep 26 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-45
- luminous: osd: change log level when withholding pg creation (rhbz#1597930)
- osd,mon: increase mon_max_pg_per_osd to 250 (rhbz#1597425)
- osd: increase default hard pg limit (rhbz#1597425)

* Wed Sep 26 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-44
- mds: print is_laggy message once (rhbz#1624527)
- mon: test if gid exists in pending for prepare_beacon (rhbz#1624527)
- msg: lower verbosity on normal event (rhbz#1624646)
- MDSMonitor: fix compile error (rhbz#1614526)
- mds: use fast dispatch to handle MDSBeacon (rhbz#1614526)
- mds: report lagginess at lower debug (rhbz#1614526)
- MDSMonitor: note beacons and cluster changes at low dbg level (rhbz#1614526)
- MDSMonitor: clean up use of pending fsmap in uncommitted ops (rhbz#1614526)
- MDSMonitor: refactor last_beacons to use mono_clock (rhbz#1614526)
- mds: refactor MDSMap init (rhbz#1614526)
- mds: refactor FSMap init (rhbz#1614526)
- mds: refactor Filesystem init (rhbz#1614526)
- mds: move compat set methods to MDSMap (rhbz#1614526)
- mon: respect standby_for_fscid when choosing standby replay mds (rhbz#1614526)
- mon: fix standby replay in multimds setup (rhbz#1614526)
- MDSMonitor: cleanup and protect fsmap access (rhbz#1614526)
- mds: mark beacons as high priority (rhbz#1614526)

* Wed Sep 26 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-43
- mds: fix unhealth heartbeat during rejoin (rhbz#1614498)

* Thu Aug 30 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-42
- rgw: fix injectargs for objecter_inflight_ops (rhbz#1591877)

* Tue Aug 28 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-41
- rgw: raise default rgw_curl_low_speed_time to 300 seconds (rhbz#1619189)

* Thu Aug 23 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-40
- luminous: mgr/MgrClient: Protect daemon_health_metrics (rhbz#1580300)

* Mon Aug 13 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-39
- mds: update MDSRank::cluster_degraded before handling mds failure (rhbz#1611056)
- qa/tasks/cephfs: add test for discontinuous mdsmap (rhbz#1601138)
- mds: handle discontinuous mdsmap (rhbz#1601138)
- mds: introduce MDSMap::get_mds_set_lower_bound() (rhbz#1601138)
- mds: avoid traversing all dirfrags when trying to get wrlocks (rhbz#1607583)
- mds: increase debug level for dropped client cap msg (rhbz#1607596)
- mds: dump recent events on respawn (rhbz#1607601)
- mds: print mdsmap processed at low debug level (rhbz#1607606)

* Tue Jul 31 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-38
- mon/OSDMonitor: Warn if missing expected_num_objects (rhbz#1592497)
- mon/OSDMonitor: Warn when expected_num_objects will have no effect (rhbz#1592497)

* Fri Jul 27 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-37
- ceph-volume: Restore SELinux context (rhbz#1609427)

* Fri Jul 27 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-36
- rgw: continue enoent index in dir_suggest (rhbz#1609030)
- rgw: fix index update in dir_suggest_changes (rhbz#1609030)

* Wed Jul 25 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-35
- rgw: set default objecter_inflight_ops = 24576 (rhbz#1591877)
- rgw: fix gc may cause a large number of read traffic (rhbz#1601068)
- rgw: add curl_low_speed_limit and curl_low_speed_time config to avoid the thread hangs in data sync. (rhbz#1589545)
- radosgw-admin: 'sync error trim' loops until complete (rhbz#1600702)
- rgw: do not ignore EEXIST in RGWPutObj::execute (rhbz#1537737)
- rgw: change default rgw_thread_pool_size to 512 (rhbz#1591822)
- rgw: add option for relaxed region enforcement (rhbz#1585307)

* Mon Jul 23 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-34
- prometheus: Set the response header for cached response (rhbz#1537505)
- prometheus: Reset the time the data was captured (rhbz#1537505)
- prometheus: Format metrics in the collect function (rhbz#1537505)
- prometheus: Remove the Metrics class (rhbz#1537505)
- prometheus: Optimize metrics formatting (rhbz#1537505)
- prometheus: Use instance instead of inst variable (rhbz#1537505)
- prometheus: Make the cache timeout configurable (rhbz#1537505)
- prometheus: Fix metric resets (rhbz#1537505)

* Wed Jul 18 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-33
- Allow swift acls to be deleted. (rhbz#1590450)

* Thu Jul 12 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-32
- ceph-disk: revise the help message for "prepare" command (rhbz#1572722)

* Wed Jul 11 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-31
- client:  update inode fields according to issued caps (rhbz#1594283)
- mds: fix occasional dir rstat inconsistency between multi-MDSes (rhbz#1594283)
- mds: don't report slow request for blocked filelock request (rhbz#1594674)
- mds: send cap export message when exporting non-auth caps to auth mds (rhbz#1594457)
- common/DecayCounter: set last_decay to current time when decoding decay counter (rhbz#1593322)
- mds: include nfiles/nsubdirs of directory inode in MClientCaps (rhbz#1594741)
- mds: fix leak of MDSCacheObject::waiting (rhbz#1594307)
- mds: fix some memory leak (rhbz#1594307)
- mds: properly trim log segments after scrub repairs something (rhbz#1593093)

* Wed Jul 11 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-30
- client: fix issue of revoking non-auth caps (rhbz#1594868)
- qa/tasks/cephfs: add timeout parameter to kclient umount_wait (rhbz#1594323)
- mds: reply session reject for open request from blacklisted client (rhbz#1594323)
- mds: set could_consume to false when no purge queue item actually executed (rhbz#1593311)
- qa/tasks/cephfs: add test for renewing stale session (rhbz#1593123)
- client: invalidate caps and leases when session becomes stale (rhbz#1593123)
- client: fix race in concurrent readdir (rhbz#1593123)
- mds: properly reconnect client caps after loading inodes (rhbz#1593100)
- mds: filter out blacklisted clients when importing caps (rhbz#1593100)
- mds: don't add blacklisted clients to reconnect gather set (rhbz#1593100)
- mds: combine MDCache::{cap_exports,cap_export_targets} (rhbz#1593100)
- mon/MDSMonitor: do not send redundant MDS health messages to cluster log (rhbz#1593031)

* Wed Jul 11 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-29
- osd/PrimaryLogPG: rebuild attrs from clients (rhbz#1599859)

* Wed Jul 11 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-28
- osd/filestore: Change default filestore_merge_threshold to -10 (rhbz#1591873)

* Thu Jun 28 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-27
- qa/workunits/rados: test pool op permissions (rhbz#1593594)
- qa/workunits/rbd: test self-managed snapshot create/remove permissions (rhbz#1593594)
- pybind/rados: new methods for manipulating self-managed snapshots (rhbz#1593594)
- mon/OSDMonitor: enforce caps for all remaining pool ops (rhbz#1593594)
- mon/OSDMonitor: enforce caps when creating/deleting unmanaged snapshots (rhbz#1593594)

* Tue Jun 26 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-26
- rgw: Silence maybe-uninitialized false positives (rhbz#1580497)
- rgw: bucket sync only allows one olh op at a time (rhbz#1580497)
- rgw: bucket sync updates high marker for squashed entries (rhbz#1580497)
- rgw: CompleteMultipart applies its olh_epoch (rhbz#1580497)
- rgw: bucket sync allows OP_ADD on versioned objects (rhbz#1580497)
- rgw: bucket sync doesn't squash over olh entries (rhbz#1580497)
- rgw: bucket sync only provides an epoch for olh operations (rhbz#1580497)
- rgw: SyncModule::sync_object() takes optional olh epoch (rhbz#1580497)
- rgw: fetch_remote_obj() applies olh even if object is current (rhbz#1580497)
- rgw: fetch_remote_obj() takes optional olh epoch (rhbz#1580497)
- rgw: Object::Write::_do_write_meta() takes optional olh epoch (rhbz#1580497)
- test/rgw: test incremental sync of acls on versioned object (rhbz#1580497)

* Tue Jun 05 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-25
- mgr: expose avg data for long running avgs (rhbz#1554281)

* Tue Jun 05 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-24
- rgw: aws4 auth supports PutBucketRequestPayment (rhbz#1569694)

* Mon Jun 04 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-23
- rgw: update ObjectCacheInfo::time_added on overwrite (rhbz#1585750)
- rgw: ObjectCache::put avoids separate find + insert (rhbz#1585750)

* Fri Jun 01 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-22
- librbd: commit IO as safe when complete if writeback cache is disabled (rhbz#1585192)

* Fri Jun 01 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-21
- librbd: commit IO as safe when complete if writeback cache is disabled (rhbz#1585192)

* Fri Jun 01 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-20
- client: delay dentry trimming until after cap traversal (rhbz#1585031)
- qa: test for trim_caps segfault for trimmed dentries (rhbz#1585031)
- client: avoid freeing inode when it contains TX buffer heads (rhbz#1585029)
- osdc/ObjectCacher: allow discard to complete in-flight writeback (rhbz#1585029)
- mds: tighten conditions of calling rejoin_gather_finish() (rhbz#1585023)
- mds: avoid calling rejoin_gather_finish() two times successively (rhbz#1585023)

* Wed May 30 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-19
- Modified mgr_module-Deal-with-long-running-avgs-properly.patch
  (rhbz#1554281)

* Wed May 30 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-18
- doc/prometheus: Mention the long running avg types (rhbz#1554281)
- prometheus: Expose sum/count pairs for avgs (rhbz#1554281)
- mgr_module: Deal with long running avgs properly (rhbz#1554281)
- mgr: Expose avgcount for long running avgs (rhbz#1554281)
- filestore: Raise the priority of two counters (rhbz#1554281)
- rgw: add configurable AWS-compat invalid range get behavior (rhbz#1583835)

* Wed May 30 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-17
- auth/cephx/CephxProtocol: better random
- cephx: update docs
- auth/cephx: add authorizer challenge (CVE-2018-1128)
- mon,msg: implement cephx_*_require_version options
- auth/cephx/CephxSessionHandler: implement CEPHX_V2 calculation mode
  (CVE-2018-1129)
- include/ceph_features: define CEPHX2 feature
- msg/async,simple: include MGR as service when applying cephx settings

* Fri May 25 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-16
- osd/osd_types: fix object_stat_sum_t decode (rhbz#1581564)

* Wed May 23 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-15
- rgw: require --yes-i-really-mean-it to run radosgw-admin orphans find (rhbz#1573657)
- mds: properly check auth subtree count in MDCache::shutdown_pass() (rhbz#1578142)
- mds: don't discover inode/dirfrag when mds is in 'starting' state (rhbz#1578142)

* Wed May 23 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-14
- rgw: require --yes-i-really-mean-it to run radosgw-admin orphans find (rhbz#1573657)
- mds: properly check auth subtree count in MDCache::shutdown_pass() (rhbz#1566016)
- mds: don't discover inode/dirfrag when mds is in 'starting' state (rhbz#1566016)

* Tue May 22 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-13
- selinux: Allow ceph to block suspend (rhbz#1565416)
- selinux: Allow ceph to execute ldconfig (rhbz#1565416)
- prometheus: Fix order of occupation values (rhbz#1554281)

* Mon May 21 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-12
- rgw: require --yes-i-really-mean-it to run radosgw-admin orphans find (rhbz#1573657)

* Mon May 21 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-11
- rgw: require --yes-i-really-mean-it to run radosgw-admin orphans find (rhbz#1573656)

* Tue May 15 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-10
- qa/cephfs: test if evicted client unmounts without hanging (rhbz#1576861)
- qa/tasks: allow custom timeout for umount_wait() (rhbz#1576861)
- client: don't hang when MDS sessions are evicted (rhbz#1576861)

* Tue May 15 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-9
- mds: kick rdlock if waiting for dirfragtreelock (rhbz#1566016)
- mds: properly check auth subtree count in MDCache::shutdown_pass() (rhbz#1566016)
- mds: don't discover inode/dirfrag when mds is in 'starting' state (rhbz#1566016)
- qa: get status to handle older api (rhbz#1572555)
- qa: backport helper functions (rhbz#1572555)
- mds: handle imported session race (rhbz#1572555)
- mds: check for session import race (rhbz#1572555)

* Mon May 14 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-8
- doc/mgr/prometheus: add instructions to correlate metrics (rhbz#1554281)
- pybind/mgr/prometheus: unify label names, move away from "id" (rhbz#1554281)
- prometheus: Expose number of degraded/misplaced/unfound objects (rhbz#1554281)
- mgr: Expose pg_sum in pg_summary (rhbz#1554281)
- prometheus: Handle the TIME perf counter type metrics (rhbz#1554281)
- prometheus: Fix prometheus shutdown/restart (rhbz#1554281)

* Fri May 11 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-7
- rgw-admin: support for processing all gc objects including unexpired. (rhbz#1548564)
- radosgw-admin: rename 'bucket sync status' to 'bucket sync markers' (rhbz#1466956)
- doc: update radosgw-admin.rst and help.t about data sync status (rhbz#1466956)
- rgw: display data sync recovering shards in radosgw-admin sync status (rhbz#1466956)
- rgw: add RGWReadDataSyncRecoveringShardsCR to read recovering shards (rhbz#1466956)
- qa/workunits/rados/test_large_omap_detection: Scrub pgs instead of OSDs (rhbz#1569192)

* Thu May 10 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-6
- rgw-admin: support for processing all gc objects including unexpired. (rhbz#1548564)
- radosgw-admin: rename 'bucket sync status' to 'bucket sync markers' (rhbz#1466956)
- doc: update radosgw-admin.rst and help.t about data sync status (rhbz#1466956)

* Thu May 10 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-5
- restful: Fix jsonification (rhbz#1506102)
- restful: Set the value of the argument (rhbz#1506102)
- restful: Support auid pool argument (rhbz#1506102)
- qa/restful: Test pg_num/pgp_num modifications (rhbz#1506102)

* Wed May 09 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-4
- rgw: use vector for remove_tags in gc aio (rhbz#1548564)
- rgw: gc aio, replace lists with other types (rhbz#1548564)
- rgw: make gc concurrenct io size configurable (rhbz#1548564)
- rgw: trim gc index using aio (rhbz#1548564)
- rgw: use a single gc io manager for all shards (rhbz#1548564)
- rgw: use aio for gc processing (rhbz#1548564)
- rgw-admin: support for processing all gc objects including unexpired. (rhbz#1548564)

* Wed May 09 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-3
- radosgw-admin: add pretty 'bucket sync status' command (rhbz#1466956)
- rgw: expose struct bucket_index_marker_info in header (rhbz#1466956)
- rgw: rgw_bucket_sync_status takes bucket info (rhbz#1466956)
- radosgw-admin: rename 'bucket sync status' to 'bucket sync markers' (rhbz#1466956)
- rgw: translate the state in rgw_data_sync_marker (rhbz#1466956)
- doc: update radosgw-admin.rst and help.t about data sync status (rhbz#1466956)
- rgw: add --shard-id for data sync status (rhbz#1466956)
- rgw: read behind bucket shards of a specified data log shard (rhbz#1466956)
- rgw: display data sync recovering shards in radosgw-admin sync status (rhbz#1466956)
- rgw: add RGWReadDataSyncRecoveringShardsCR to read recovering shards (rhbz#1466956)
- rgw: display errors of object sync failed in sync error list (rhbz#1466956)
- rgw: add lagging shard ids in rgw sync status (rhbz#1466956)
- rgw: RGWRadosGetOmapKeysCR uses omap_get_keys2 (rhbz#1466956)
- rgw: RGWRadosGetOmapKeysCR uses completion return code (rhbz#1466956)
- qa: ignore version in auth metadata comp (rhbz#1566194)
- ceph_volume_client: allow volumes without namespace isolation (rhbz#1566194)
- mon/PGMap: Summarise OSDs in blocked/stuck requests (rhbz#1576204)
- qa/workunits/rados/test_large_omap_detection: Scrub pgs instead of OSDs (rhbz#1569192)
- osd: Add a flag to ScrubMap to signal check needed (rhbz#1569192)
- osd: Warn about objects with too many omap entries (rhbz#1569192)
- osd: Move creation of 'master_set' to scrub_compare_maps (rhbz#1569192)

* Wed May 09 2018 Ken Dreyer <kdreyer@redhat.com> - 2:12.2.5-2
- Drop ExclusiveArch x86_64 (rhbz#1563510)

* Tue May 08 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.5-1
- Update to v12.2.5 (rhbz#1571353)
- rgw: ability to list bucket contents in unsorted order for efficiency
  (rhbz#1548563)
- rgw: consolidate code that implements hashing algorithms (rhbz#1548563)
- rgw: add buffering filter to compression for fetch_remote_obj (rhbz#1501380)
- ceph-disk: default to --filestore (rhbz#1572722)

* Wed May 02 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-10
- rgw: raise log level on coroutine shutdown errors (rhbz#1499324)
- rgw: fix bi_list to reset is_truncated flag if it skips entires (rhbz#1554221)
- rgw: fix use of libcurl with empty header values (rhbz#1561531)

* Thu Apr 26 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-9
- fuse: wire up fuse_ll_access (rhbz#1560575)
- client: remove getgroups_cb (rhbz#1560575)
- client: remove _getgrouplist (rhbz#1560575)
- client: have init_gids just set alloced_gids to true (rhbz#1560575)
- client: remove init_groups (rhbz#1560575)
- fuse: handle errors appropriately when getting group list (rhbz#1560575)

* Thu Apr 26 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-8
- client: flush the mdlog in _fsync before waiting on unstable reqs (rhbz#1566467)
- mds: don't try exporting subdir if dirfrag is already being exported (rhbz#1554593)
- mds: always pass current time to MDBalancer::{hit_inode,hit_dir} (rhbz#1554593)
- Make MDS evaluates the overload situation with the same criterion (rhbz#1554593)
- discard the mdsload clear after prep_rebalance in case we want to export it for debugging (rhbz#1554593)
- make sure that MDBalancer uses heartbeat info from the same epoch (rhbz#1554593)
- mds: don't cleanup request that has pending remote authpin/wrlock/xlock (rhbz#1559749)

* Thu Apr 26 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-7
- client: flush the mdlog in _fsync before waiting on unstable reqs (rhbz#1566467)
- client: add ceph_ll_sync_inode (rhbz#1566467)
- mds: limit run time of load balancer (rhbz#1554593)
- mds: add list to track recently used sub-directories (rhbz#1554593)
- mds: calculate other mds' last_epoch_under locally (rhbz#1554593)
- mds: cleanup mds_load map access/update (rhbz#1554593)
- mds: check export pin when choosing dirfrags for exporting (rhbz#1554593)
- mds: optimize MDBalancer::find_exports() (rhbz#1554593)
- mds: avoid creating unnecessary subtrees during load balance (rhbz#1554593)
- mds: mds: optimize MDBalancer::try_rebalance() (rhbz#1554593)
- mds: don't try exporting subdir if dirfrag is already being exported (rhbz#1554593)
- mds: don't try exporting dirfrags under mds's own mdsdir (rhbz#1554593)
- mds: cleanup MDBalancer::try_rebalance() (rhbz#1554593)
- mds: always pass current time to MDBalancer::{hit_inode,hit_dir} (rhbz#1554593)
- mds: remove unused MDBalancer::export_empties() (rhbz#1554593)
- mds: adjust subtree popularity after rename (rhbz#1554593)
- mds: fix request rate calculation (rhbz#1554593)
- simplify mds overload judgement logic (rhbz#1554593)
- Make MDS evaluates the overload situation with the same criterion (rhbz#1554593)
- mds: add asok command that dumps metadata popularity (rhbz#1554593)
- discard the mdsload clear after prep_rebalance in case we want to export it for debugging (rhbz#1554593)
- make sure that MDBalancer uses heartbeat info from the same epoch (rhbz#1554593)
- make popular counter decay at proper rate (rhbz#1554593)
- mds: various fixes for backport (rhbz#1531679)
- mds: convert to boost::string_view (rhbz#1531679)
- test/encoding: refactor to avoid escaping shell magic (rhbz#1531679)
- mds: minor refactor of SimpleLock (rhbz#1531679)
- mds: track Capability in mempool (rhbz#1531679)
- mds: move CInode container members to mempool (rhbz#1531679)
- mds: move CDentry container members to mempool (rhbz#1531679)
- mds: move CDir container members to mempool (rhbz#1531679)
- mds: put MDSCacheObject compact_map in mempool (rhbz#1531679)
- common: use size_t for object size (rhbz#1531679)
- mds: convert to allocator agnostic string_view (rhbz#1531679)
- mds: simplify initialization (rhbz#1531679)
- compact_*: support mempool allocated containers (rhbz#1531679)
- mds: always handle SESSION_REQUEST_RENEWCAPS messages (rhbz#1559749)
- mds: don't cleanup request that has pending remote authpin/wrlock/xlock (rhbz#1559749)
- mds: reset connection's priv when marking down connection (rhbz#1559749)
- mds: fix session reference leak (rhbz#1559749)
- fuse: wire up fuse_ll_access (rhbz#1560575)

* Thu Apr 05 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-6
- Drop patch that reverted PR #18782 (rhbz#1550026)

* Thu Apr 05 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-5
- mds: bump mds_log_max_segments for trim buffer (rhbz#1507629)

* Mon Mar 19 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-4
- qa: ignore bad backtrace cluster wrn (rhbz#1518730)
- qa/cephfs: Add tests to validate scrub functionality (rhbz#1518730)
- cephfs: Add option to load invalid metadata from disk (rhbz#1518730)
- cephfs: Reset scrub data when inodes move (rhbz#1518730)

* Thu Mar 15 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-3
- Revert "Merge pull request #18782 from ukernel/luminous-21985" (rhbz#1550026)

* Wed Mar 14 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-2
- PrimaryLogPG: only trim up to osd_pg_log_trim_max entries at once (rhbz#1554544)
- PG, PrimaryLogPG: trim log and rollback info for error log entries (rhbz#1554544)
- tools: Add pg log trim command to ceph-objectstore-tool (rhbz#1552094)

* Mon Mar 12 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.4-1
- Update to v12.2.4 (rhbz#1548067 rhbz#1325322 rhbz#1489866 rhbz#1493418
  rhbz#1506438 rhbz#1507136 rhbz#1507629 rhbz#1538317 rhbz#1541424
  rhbz#1543879 rhbz#1544680)

* Thu Mar 08 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-46
- rgw:  make init env methods return an error (rhbz#1547673)

* Tue Feb 27 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-45
- osd: Only scan for omap corruption once (rhbz#1549293)
- tools: Add --backend option to ceph-osdomap-tool default to rocksdb (rhbz#1549293)
- osd, mds, tools: drop the invalid comment and some unused variables (rhbz#1549293)
- tools: Add the ability to reset state to v2 (rhbz#1549293)
- tools: Show DB state information (rhbz#1549293)

* Wed Jan 24 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-44
- rgw: Fix swift object expiry not deleting objects (rhbz#1530673)

* Thu Jan 11 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-43
- config: lower default omap entries recovered at once (rhbz#1505559)

* Wed Jan 10 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-42
- rgw: dont log EBUSY errors in 'sync error list' (rhbz#1530665)

* Mon Jan 08 2018 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-41
- rgw: put bucket policy panics RGW process (rhbz#1531673)
- rgw: Plumb refresh logic into object cache (rhbz#1530801)
- rgw: Add expiration in the object cache (rhbz#1530801)
- rgw: retry CORS put/delete operations on ECANCELLED (rhbz#1530801)
- rgw: Expire entries in bucket info cache (rhbz#1530801)
- rgw: Handle stale bucket info in RGWDeleteBucketPolicy (rhbz#1530801)
- rgw: Handle stale bucket info in RGWPutBucketPolicy (rhbz#1530801)
- rgw: Handle stale bucket info in RGWDeleteBucketWebsite (rhbz#1530801)
- rgw: Handle stale bucket info in RGWSetBucketWebsite (rhbz#1530801)
- rgw: Handle stale bucket info in RGWSetBucketVersioning (rhbz#1530801)
- rgw: Handle stale bucket info in RGWPutMetadataBucket (rhbz#1530801)
- rgw: Add retry_raced_bucket_write (rhbz#1530801)
- rgw: Add try_refresh_bucket_info function (rhbz#1530801)
- rgw: fix rewrite a versioning object create a new object bug (rhbz#1531279)
- rgw: fix chained cache invalidation to prevent cache size growth above the rgw_cache_lru_size limit (rhbz#1530670)
- RGW: S3 POST policy should not require Content-Type (rhbz#1530775)
- rgw: fix BZ 1500904, Stale bucket index entry remains after object deletion (rhbz#1530784)
- ceph.in: pass RADOS inst to LibCephFS (rhbz#1491170)

* Wed Nov 22 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-40
- rgw: set num_shards on 'radosgw-admin data sync init' (rhbz#1512092)
- dencoder/rgw: expose rgw sync status types (rhbz#1512092)

* Thu Nov 02 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-39
- Revert "rgw_file: disable FLAG_EXACT_MATCH enforcement" (rhbz#1509035)

* Thu Nov 02 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-38
- rgw: add missing current_history initialization (rhbz#1508322)
- rgw: init oldest period after setting run_sync_thread (rhbz#1508322)

* Wed Nov 01 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-37
- rgw:fix list objects with marker when bucket is enable versioning (rhbz#1508615)

* Wed Nov 01 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-36
- rgw: remove placement_rule from cls_user_bucket_entry (rhbz#1506239)
- rgw: remove placement_rule from rgw_link_bucket() (rhbz#1506239)
- rgw: take placement_rule from bucket info in update_containers_stats (rhbz#1506239)
- cmake/cls: add install() for ceph_test_cls_log (rhbz#1507650)
- qa: add ceph_test_cls_log to cls workunit (rhbz#1507650)
- osd: add processed_subop_count for cls_cxx_subop_version() (rhbz#1507650)

* Tue Oct 31 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-35
- rgw: fix extra_data_len handling in PutObj filters (rhbz#1505485)

* Mon Oct 30 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-34
- rgw_file:  set s->obj_size from bytes_written (rhbz#1507128)

* Mon Oct 30 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-33
- rgw: Fix dereference of empty optional (rhbz#1503280)

* Fri Oct 27 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-32
- Update "cls/journal: fixed possible infinite loop in expire_tags" patch
  (rhbz#1501374)

* Fri Oct 27 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-31
- cls/journal: fixed possible infinite loop in expire_tags (rhbz#1501374)

* Thu Oct 26 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-30
- rgw: include SSE-KMS headers in encrypted upload response (rhbz#1496460)

* Wed Oct 25 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-29
- rgw: dont reuse stale RGWObjectCtx for get_bucket_info() (rhbz#1506239)

* Wed Oct 25 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-28
- Drop "radosgw: fix awsv4 header line sort order." (rhbz#1498323)

* Wed Oct 25 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-27
- You can find the problem do like this: (rhbz#1505504)

* Tue Oct 24 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-26
- rbd-mirror: strip environment/CLI overrides for remote cluster (rhbz#1505496)

* Mon Oct 23 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-25
- buffer: remove list _mempool member (rhbz#1505460)
- buffer: allow mempool to be passed into raw* ctors and create methods (rhbz#1505460)
- messages/MOSDMap: do compat reencode of crush map, too (rhbz#1505365)

* Mon Oct 23 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-24
- osdc/Objecter: skip sparse-read result decode if bufferlist is empty (rhbz#1496674)
- osdc/Objecter: delay initialization of hobject_t in _send_op (rhbz#1496674)
- common/common_init: disable ms subsystem log gathering for clients (rhbz#1496674)

* Thu Oct 19 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-23
- rgw_file: disable FLAG_EXACT_MATCH enforcement (rhbz#1489452)
- rgw_file: implement variant offset readdir processing (rhbz#1489452)

* Thu Oct 19 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-22
- os/bluestore: move several buffer{ptr,list}s into cache_other mempool (rhbz#1504179)
- os/bluestore: put new attrs in correct mempool too (rhbz#1504179)
- os/bluestore: put attrs in mempool (rhbz#1504179)
- buffer: add ptr::[try_]reassign_to_mempool (rhbz#1504179)
- os/bluestore: add bluestore_bluefs_min_free (rhbz#1504179)
- os/bluestore/BlueFS: crash on enospc (rhbz#1504179)
- os/bluestore: use normal Context for async deferred_try_submit (rhbz#1504179)
- os/bluestore: wake kv thread when blocking on deferred_bytes (rhbz#1504179)
- osd: make shutdown debug conditional (and off by default) (rhbz#1504179)
- osd: debug_bluestore on shutdown (rhbz#1504179)
- os/bluestore: dump stray cache content on shutdown (rhbz#1504179)
- os/bluestore: ignore 0x2000~2000 extent oddity from luminous upgrade (rhbz#1504179)
- os/bluestore: use min_alloc_size for freelist resolution (rhbz#1504179)
- os/bluestore: align bluefs_extents to min_alloc_size (rhbz#1504179)
- os/bluestore/FreelistManager: create: accept min alloc size (rhbz#1504179)
- os/bluestore: mkfs: choose min_alloc_size earlier (rhbz#1504179)
- os/bluestore: require that bluefs_alloc_size be multiple of min_alloc_size (rhbz#1504179)
- os/bluestore: allocate entire write in one go (rhbz#1504179)
- ceph-bluestore-tool: better default logging; --log-file and --log-level options (rhbz#1504179)
- ceph-bluestore-tool: add 'bluefs-bdev-expand' to expand wal or db usage (rhbz#1504179)
- ceph-bluestore-tool: add 'bluefs-bdev-sizes' command (rhbz#1504179)
- os/ObjectStore: add repair interface (rhbz#1504179)
- ceph-objectstore-tool: Make pg removal require --force (rhbz#1504179)
- ceph-bluestore-tool: factor out bluefs mount (rhbz#1504179)
- os/bluestore: repair 21089 on freelist init (rhbz#1504179)
- os/bluestore: fsck: remove fsck repair for 21089 (rhbz#1504179)
- os/bluestore/KernelDevice: hack to inject bad device size (rhbz#1504179)
- osd: make the PG's SORTBITWISE assert a more generous shutdown (rhbz#1504177)
- src/messages/MOSDMap: reencode OSDMap for older clients (rhbz#1504172)
- mon/MgrMonitor: read cmd descs if empty on update_from_paxos() (rhbz#1504171)
- mon/MgrMonitor: populate on-disk cmd descs if empty on upgrade (rhbz#1504171)
- rbd-mirorr: does not start on reboot (rhbz#1504166)

* Wed Oct 18 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-21
- rgw_file: explicit NFSv3 open() emulation (rhbz#1492582)

* Tue Oct 17 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-20
- rgw: Remove assertions in IAM Policy (rhbz#1503280)

* Tue Oct 17 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-19
- rgw: disable dynamic resharding in multisite environment (rhbz#1498474)
- cls/rgw: increment header version to avoid overwriting bilog entries (rhbz#1501408)

* Tue Oct 17 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-18
- test/rgw: add test_multipart_object_sync (rhbz#1501408)
- cls/rgw: increment header version to avoid overwriting bilog entries (rhbz#1501408)

* Mon Oct 16 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-17
- cls/journal: fixed possible infinite loop which could kill the OSD (rhbz#1501374)
- test: ceph_test_cls_journal was dropped when converting to cmake (rhbz#1501374)

* Mon Oct 16 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-16
- mds: prevent trim count from underflowing (rhbz#1502178)
- common/options: enable multiple rocksdb compaction threads for filestore (rhbz#1502763)
- common/options.cc: Set Filestore rocksdb compaction readahead option. (rhbz#1502763)
- doc/rados/operations/health-checks: fix TOO_MANY_PGS discussion (rhbz#1489064)
- mon: rename mon_pg_warn_max_per_osd -> mon_max_pg_per_osd (rhbz#1489064)
- qa/standalong/mon/osd-pool-create: fewer pgs in test (rhbz#1489064)
- mon/OSDMonitor: assume a minimum cluster size of 3 (rhbz#1489064)
- mon/OSDMonitor: prevent pg_num from exceeding mon_pg_warn_max_per_osd (rhbz#1489064)
- common/options: reduce mon_pg_warn_max_per_osd to 200 (rhbz#1489064)
- rgw: calculate and print Swift's X-Account-Storage-Policy-* headers. (rhbz#1436386)
- rgw: bucket linking stores also the info about a placement rule. (rhbz#1436386)
- rgw: convey placement rule in RGWBucketEnt and cls_user_bucket_entry. (rhbz#1436386)
- rgw: clean-up around and implement the move semantics in RGWBucketEnt. (rhbz#1436386)
- rgw: enforce the std::move semantic across the path of RGWUserBuckets. (rhbz#1436386)
- rgw: {end_}marker params are handled during Swift's reversed account listing. (rhbz#1436386)
- rgw: add basic support for Swift's reversed account listings. (rhbz#1436386)
- rgw: abstract partial data processing in RGWListBuckets. (rhbz#1436386)
- rgw: rename the configurables for metadata limits to start with rgw_. (rhbz#1436386)
- rgw: return proper message when deleting non-empty Swift's container. (rhbz#1436386)
- rgw: seed::get_torrent_file returns errors in the usual way. (rhbz#1436386)
- rgw: add support for max_meta_count of Swift API's /info. (rhbz#1436386)
- rgw: Swift API returns 400 Bad Request on too long container names. (rhbz#1436386)
- rgw: honor custom rgw_err::message in Swift's error handling. (rhbz#1436386)
- rgw: add support for max_meta_value_length of Swift API's /info. (rhbz#1436386)
- rgw: refactor rgw_get_request_metadata to reduce the number of dynallocs. (rhbz#1436386)
- rgw: add support for max_meta_name_length of Swift API's /info. (rhbz#1436386)
- rgw: list_objects() honors end_marker regardless of namespace. (rhbz#1436386)
- osdc/ObjectCacher: limit memory usage of BufferHead (rhbz#1490814)
- mds: keep CInode::STATE_QUEUEDEXPORTPIN state when exporting inode (rhbz#1500874)

* Fri Oct 13 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-15
- rgw: 'zone placement' commands validate compression type (rhbz#1501389)

* Wed Oct 11 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-14
- rgw: RGWUser::init no longer overwrites user_id (rhbz#1489391)

* Wed Oct 11 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-13
- ceph-disk: retry on OSError (rhbz#1494543)
- ceph-disk: factor out the retry logic into a decorator (rhbz#1494543)

* Tue Oct 10 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-12
- rgw: encryption add exception handling for from_base64 on bad input (rhbz#1496460)
- rgw: encryption fix the issue when not provide encryption mode (rhbz#1496460)
- rgw: encryption SSE-KMS add the details of error msg in response (rhbz#1496460)
- rgw: encryption SSE-C add the details of error msg in response (rhbz#1496460)

* Tue Oct 10 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-11
- librbd: refresh image after applying new/removing old metadata (rhbz#1493977)

* Thu Oct 05 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-10
- osd: additional protection for out-of-bounds EC reads (rhbz#1498611)
- RGW: Multipart upload may double the quota (rhbz#1498668)
- RGW: fix a bug about inconsistent unit of comparison (rhbz#1498668)
- rgw: release cls lock if taken in RGWCompleteMultipart (rhbz#1497853)
- librbd: avoid dynamically refreshing non-atomic configuration settings (rhbz#1493977)
- librbd: notify watcher when updating image metadata (rhbz#1493977)
- rbd-mirror: sync image metadata when transfering remote image (rhbz#1493977)
- librbd: snapshots should be created/removed against data pool (rhbz#1497332)
- radosgw: fix awsv4 header line sort order. (rhbz#1498323)

* Mon Oct 02 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-9
- selinux: Allow getattr on lnk sysfs files (rhbz#1493750)

* Thu Sep 28 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-8
- rbd: mirror "get" actions now have cleaner error messages (rhbz#1492785)
- cls/rbd: avoid recursively listing the watchers on rbd_mirroring object (rhbz#1492785)

* Thu Sep 28 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-7
- rbd-mirror: ensure forced-failover cannot result in sync state (rhbz#1495521)
- rbd-mirror: forced-promotion should interrupt replay delay to shut down (rhbz#1495521)

* Thu Sep 28 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-6
- rgw: Check payment operations in policy (rhbz#1490278)
- rgw: Check bucket versioning operations in policy (rhbz#1490278)

* Thu Sep 28 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-5
- rgw: Check bucket GetBucketLocation in policy (rhbz#1493934)

* Thu Sep 28 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-4
- rgw: Check bucket Website operations in policy (rhbz#1493896)

* Thu Sep 28 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-3
- rgw: Check bucket CORS operations in policy (rhbz#1494140)
- ceph_volume_client: perform snapshot operations in (rhbz#1494980)

* Wed Sep 27 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.1-2
- rgw_file: fix write error when the write offset overlaps. (rhbz#1496585)

* Wed Sep 27 2017 Ken Dreyer <kdreyer@redhat.com> - 2:12.2.1-1
- Update to v12.2.1 (rhbz#1472464 rhbz#1472465 rhbz#1477311 rhbz#1464976
  rhbz#1492865 rhbz#1489461 rhbz#1480182 rhbz#1485783 rhbz#1468031)

* Wed Sep 06 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.2.0-2
- ceph-volume tests add new ceph_* ansible dev variables required (centos) (rhbz#1485011)
- ceph-volume tests add new ceph_* ansible dev variables required (xenial) (rhbz#1485011)
- ceph-volume util create a disk utility for blkid operations (rhbz#1485011)
- ceph-volume lvm.prepare store the blkid uuid of a partition journal (rhbz#1485011)
- ceph-volume lvm.activate use the partuuid of a partition to link the journal (rhbz#1485011)
- ceph-volume tests update the ansible version for functional/tox.ini (rhbz#1485011)
- ceph-volume tests add pv* related unit tests (rhbz#1485011)
- ceph-volume lvm.api include lv_uuid as output fields (rhbz#1485011)
- ceph-volume lvm.activate always update the link to the journal (rhbz#1485011)
- ceph-volume lvm.activate retrieve the journal uuid if journal is a device (rhbz#1485011)
- ceph-volume exceptions create a specifc error for multiple pvs (rhbz#1485011)
- ceph-volume lvm.prepare make a journal a pv, use uuids always (rhbz#1485011)
- ceph-volume lvm.api create the PVolumes class and helpers (rhbz#1485011)
- ceph-volume lvm.api create the PVolume class (rhbz#1485011)
- ceph-volume lvm.api add a helper to create pvs (rhbz#1485011)

* Tue Aug 29 2017 Ken Dreyer <kdreyer@redhat.com> - 2:12.2.0-1
- Update to v12.2.0 (rhbz#1484002 rhbz#1478599)

* Mon Aug 21 2017 Ken Dreyer <kdreyer@redhat.com> - 2:12.1.4-2
- ceph-fuse depends on fuse (rhbz#1479138)

* Tue Aug 15 2017 Ken Dreyer <kdreyer@redhat.com> - 2:12.1.4-1
- latest luminous rc (rhbz#1479797 rhbz#1464955 rhbz#1461041 rhbz#1451936
  rhbz#1455711 rhbz#1305670 rhbz#1464981 rhbz#1332083 rhbz#1470837)

* Wed Aug 02 2017 Ken Dreyer <kdreyer@redhat.com> - 2:12.1.2-1
- latest luminous rc (rhbz#1473386)

* Thu Jul 20 2017 Ken Dreyer <kdreyer@redhat.com> 2:12.1.1-2
- rgw_file: permit dirent offset computation (rhbz#1473386)

* Tue Jul 18 2017 Ken Dreyer <kdreyer@redhat.com> - 2:12.1.1-1
- luminous rc2 (rhbz#1470865)

* Thu Jul 06 2017 Ken Dreyer <kdreyer@redhat.com> - 1:12.1.0-1
- luminous rc1

* Fri May 19 2017 Ken Dreyer <kdreyer@redhat.com> - 1:12.0.3-1
- initial luminous pre-release package
