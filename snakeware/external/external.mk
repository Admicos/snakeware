include $(sort $(wildcard $(BR2_EXTERNAL_SNAKEWARE_PATH)/package/*/*.mk))

ifeq ($(SNAKEWARE_OPTIMIZE_PYTHON),y)
	PYTHON3_CONF_OPTS += --with-lto --enable-optimizations
endif
